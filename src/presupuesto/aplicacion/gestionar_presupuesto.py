"""Montos COP exactos con Decimal, separados por evento y propietario."""
import re
from decimal import Decimal
from sqlalchemy import select
from src.compartido.infraestructura.base_datos import SessionLocal
from src.compartido.aplicacion.acceso_evento import obtener_evento, datos_evento, texto, identificador
from src.presupuesto.infraestructura.modelos_presupuesto import PresupuestoModelo, GastoModelo


def monto(valor, permitir_cero=False):
    entrada = str(valor or "").strip().replace(",", ".")
    if not re.fullmatch(r"[0-9]{1,10}(?:\.[0-9]{1,2})?", entrada):
        raise ValueError("Escribe un monto válido, sin separadores de miles y con máximo dos decimales.")
    numero = Decimal(entrada).quantize(Decimal("0.01"))
    if numero < 0 or (numero == 0 and not permitir_cero):
        raise ValueError("El valor del gasto debe ser mayor que cero.")
    return numero


def consultar_presupuesto(evento_id, usuario_id):
    with SessionLocal() as sesion:
        evento = obtener_evento(sesion, evento_id, usuario_id)
        presupuesto = sesion.get(PresupuestoModelo, evento_id)
        modelos = sesion.scalars(select(GastoModelo).where(GastoModelo.evento_id == evento_id).order_by(GastoModelo.id.desc())).all()
        gastos = [{"id": g.id, "concepto": g.concepto, "categoria": g.categoria,
                   "notas": g.notas, "valor": g.valor, "pagado": g.pagado} for g in modelos]
        total = sum((g.valor for g in modelos), Decimal("0.00"))
        pagado = sum((g.valor for g in modelos if g.pagado), Decimal("0.00"))
        limite = presupuesto.limite if presupuesto is not None else None
        categorias = {}
        for g in modelos:
            categorias[g.categoria] = categorias.get(g.categoria, Decimal("0.00")) + g.valor
        return {"evento": datos_evento(evento), "gastos": gastos, "limite": limite,
                "total": total, "pagado": pagado, "pendiente": total - pagado,
                "saldo": limite - total if limite is not None else None,
                "porcentaje": min(100, int(total / limite * 100)) if limite else 0,
                "categorias": sorted(categorias.items())}


def modificar_presupuesto(evento_id, usuario_id, datos):
    accion = datos.get("accion", "")
    if accion not in ("limite", "crear", "editar", "pago", "eliminar"):
        raise ValueError("Acción no válida.")
    with SessionLocal.begin() as sesion:
        obtener_evento(sesion, evento_id, usuario_id, escritura=True)
        if accion == "limite":
            limite = monto(datos.get("limite"), permitir_cero=True)
            presupuesto = sesion.get(PresupuestoModelo, evento_id)
            if presupuesto is None:
                sesion.add(PresupuestoModelo(evento_id=evento_id, limite=limite))
            else:
                presupuesto.limite = limite
            return
        gasto = None
        if accion != "crear":
            gasto = sesion.scalar(select(GastoModelo).where(
                GastoModelo.id == identificador(datos.get("gasto_id")), GastoModelo.evento_id == evento_id))
            if gasto is None:
                raise LookupError("Gasto no encontrado.")
        if accion == "eliminar":
            sesion.delete(gasto)
        elif accion == "pago":
            if datos.get("estado") not in ("pagado", "pendiente"):
                raise ValueError("Estado de pago no válido.")
            gasto.pagado = datos["estado"] == "pagado"
        else:
            concepto = texto(datos.get("concepto"), "Concepto", 150)
            categoria = texto(datos.get("categoria"), "Categoría", 80)
            notas = texto(datos.get("notas"), "Notas", 2000, False)
            valor = monto(datos.get("valor"))
            if gasto is None:
                gasto = GastoModelo(evento_id=evento_id, pagado=False)
                sesion.add(gasto)
            gasto.concepto, gasto.categoria, gasto.notas, gasto.valor = concepto, categoria, notas or None, valor
