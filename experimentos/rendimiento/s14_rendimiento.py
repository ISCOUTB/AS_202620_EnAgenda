import csv
import json
import math
import os
import platform
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from importlib.metadata import version
from pathlib import Path

import requests
from sqlalchemy import select
from src.compartido.infraestructura.base_datos import SessionLocal
from src.eventos.infraestructura.modelo_evento import EventoModelo
from src.invitaciones.infraestructura.modelo_invitacion import InvitacionModelo

BASE = "http://enagenda:5000"
EVENTO = 2
CICLOS = 20

class Formulario(HTMLParser):
    def __init__(self, texto):
        super().__init__()
        self.csrf = None
        self.estado = None
        self.feed(texto)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "input" and a.get("name") == "csrf_token":
            self.csrf = a.get("value")
        if tag == "input" and a.get("name") == "estado" and "checked" in a:
            self.estado = a.get("value")


def main():
    if os.environ.get("S14_CONFIRMAR") != "EVENTO_2_LOCAL":
        raise SystemExit("Falta confirmar EVENTO_2_LOCAL; no se ejecuto la carga.")
    with SessionLocal() as db:
        url = db.get_bind().url
        if url.host != "db" or url.database != "enagenda":
            raise SystemExit("Conexion distinta de la base local esperada.")
        e = db.get(EventoModelo, EVENTO)
        if e is None or not e.titulo.strip().upper().startswith("S14"):
            raise SystemExit("El evento 2 no esta identificado como S14.")
        limite = e.fecha_limite_confirmacion
        if limite.tzinfo is None:
            limite = limite.replace(tzinfo=timezone.utc)
        if e.estado in ("finalizado", "cancelado") or limite <= datetime.now(timezone.utc):
            raise SystemExit("El evento no admite respuestas vigentes.")
        tokens = list(db.scalars(select(InvitacionModelo.token).where(
            InvitacionModelo.evento_id == EVENTO
        ).order_by(InvitacionModelo.id).limit(10)))
        if len(tokens) != 10:
            raise SystemExit("Se requieren diez invitaciones en el evento S14.")

    inicio = datetime.now(timezone.utc)
    carpeta = Path("/evidencia/docs/evidencias") / inicio.strftime("s14-local-%Y%m%dT%H%M%SZ")
    carpeta.mkdir(parents=True, exist_ok=False)
    filas = []
    recorridos = []

    def ejecutar(cliente, token, usuarios, usuario, ciclo, registrar):
        ruta = BASE + "/eventos/invitacion/" + token
        comienzo = time.perf_counter()
        esperado = None
        correcto = True
        for operacion in ("consultar", "responder", "verificar"):
            t = time.perf_counter()
            codigo = 0
            error = ""
            try:
                if operacion == "responder":
                    r = cliente.post(ruta, data={"csrf_token": formulario.csrf,
                                               "estado": esperado}, timeout=(5, 15), allow_redirects=False)
                else:
                    r = cliente.get(ruta, timeout=(5, 15), allow_redirects=False)
                codigo = r.status_code
                if codigo != 200:
                    raise ValueError("http_no_200")
                formulario = Formulario(r.text)
                if not formulario.csrf:
                    raise ValueError("formulario_sin_csrf")
                if operacion == "consultar":
                    esperado = "no_asistire" if formulario.estado == "confirmado" else "confirmado"
                elif formulario.estado != esperado:
                    raise ValueError("estado_no_coincide")
            except requests.RequestException:
                error = "error_transporte"
            except ValueError as exc:
                error = str(exc)
            ms = (time.perf_counter() - t) * 1000
            if registrar:
                filas.append({"usuarios": usuarios, "usuario": usuario, "ciclo": ciclo,
                              "operacion": operacion, "ms": round(ms, 3),
                              "http": codigo, "ok": not error, "error": error})
            if error:
                correcto = False
                break
        if registrar:
            recorridos.append({"usuarios": usuarios, "ms": (time.perf_counter()-comienzo)*1000,
                               "ok": correcto})
        return correcto

    def trabajador(n, indice, barrera):
        with requests.Session() as cliente:
            cliente.trust_env = False
            barrera.wait(timeout=30)
            for ciclo in range(1, CICLOS + 1):
                ejecutar(cliente, tokens[indice], n, indice + 1, ciclo, True)
                time.sleep(0.1)

    with requests.Session() as cliente:
        cliente.trust_env = False
        for token in tokens:
            if not ejecutar(cliente, token, 0, 0, 0, False):
                raise SystemExit("Fallo el calentamiento; no se ejecuto la medicion.")

    for n in (1, 5, 10):
        barrera = threading.Barrier(n)
        with ThreadPoolExecutor(max_workers=n) as pool:
            list(pool.map(lambda i: trabajador(n, i, barrera), range(n)))

    def resumen(datos):
        tiempos = sorted(d["ms"] for d in datos)
        return {"muestras": len(datos), "errores": sum(not d["ok"] for d in datos),
                "p95_ms": round(tiempos[math.ceil(0.95*len(tiempos))-1], 3),
                "max_ms": round(tiempos[-1], 3)}

    resultados = []
    for n in (1, 5, 10):
        peticiones = [f for f in filas if f["usuarios"] == n]
        ciclos = [r for r in recorridos if r["usuarios"] == n]
        estadisticas = {op: resumen([f for f in peticiones if f["operacion"] == op])
                        for op in ("consultar", "responder", "verificar")
                        if any(f["operacion"] == op for f in peticiones)}
        errores = sum(not f["ok"] for f in peticiones)
        resultados.append({"usuarios": n, "operaciones": estadisticas,
            "recorrido": resumen(ciclos),
            "error_pct": round(100*errores/len(peticiones), 3),
            "cumple_objetivo_operaciones": len(estadisticas) == 3 and
                all(v["p95_ms"] < 2000 and v["errores"] == 0 for v in estadisticas.values())
                and all(r["ok"] for r in ciclos)})
    with (carpeta / "peticiones.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    reporte = {"inicio_utc": inicio.isoformat(), "fin_utc": datetime.now(timezone.utc).isoformat(),
        "commit_declarado": os.environ.get("S14_COMMIT", "no_registrado"),
        "entorno": "Docker Compose local; generador en contenedor separado; sin navegador ni estaticos",
        "python_generador": platform.python_version(),
        "requests": version("requests"), "evento_id": EVENTO,
        "calentamiento": "10 recorridos excluidos", "ciclos_por_usuario": CICLOS,
        "pausa_segundos": 0.1, "modelo": "cerrado; sin tasa de llegada fija",
        "p95": "rango mas cercano; incluye intentos fallidos; tiempos HTTP completos",
        "alcance": "Un evento y diez invitados; modifica respuestas; no acredita produccion ni todo EC-05",
        "resultados": resultados}
    (carpeta / "resumen.json").write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(resultados, indent=2))
    print("Evidencia: " + carpeta.name)
    raise SystemExit(0 if all(r["cumple_objetivo_operaciones"] for r in resultados) else 1)

if __name__ == "__main__":
    main()
