"""Agenda cronológica con horario de Cartagena y sin superposiciones."""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from sqlalchemy import select
from src.compartido.infraestructura.base_datos import SessionLocal
from src.compartido.aplicacion.acceso_evento import obtener_evento, datos_evento, texto, identificador
from src.agenda.infraestructura.modelo_actividad import ActividadModelo

ZONA = ZoneInfo("America/Bogota")


def fecha_local(fecha):
    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=timezone.utc)
    return fecha.astimezone(ZONA)


def leer_fecha(valor):
    try:
        fecha = datetime.fromisoformat(valor)
    except (ValueError, TypeError):
        raise ValueError("Escribe fechas y horas válidas para la actividad.") from None
    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=ZONA)
    return fecha.astimezone(timezone.utc)


def consultar_agenda(evento_id, usuario_id):
    with SessionLocal() as sesion:
        evento = obtener_evento(sesion, evento_id, usuario_id)
        actividades = sesion.scalars(select(ActividadModelo).where(
            ActividadModelo.evento_id == evento_id
        ).order_by(ActividadModelo.inicio, ActividadModelo.id)).all()
        return {"evento": datos_evento(evento), "fecha_sugerida": fecha_local(evento.fecha_evento).strftime("%Y-%m-%d"),
                "actividades": [{"id": a.id, "titulo": a.titulo, "descripcion": a.descripcion,
                  "responsable": a.responsable, "inicio": fecha_local(a.inicio), "fin": fecha_local(a.fin)} for a in actividades]}


def modificar_agenda(evento_id, usuario_id, datos):
    accion = datos.get("accion", "")
    if accion not in ("crear", "editar", "eliminar"):
        raise ValueError("Acción no válida.")
    with SessionLocal.begin() as sesion:
        obtener_evento(sesion, evento_id, usuario_id, escritura=True)
        actividad = None
        if accion != "crear":
            actividad = sesion.scalar(select(ActividadModelo).where(
                ActividadModelo.id == identificador(datos.get("actividad_id")), ActividadModelo.evento_id == evento_id))
            if actividad is None:
                raise LookupError("Actividad no encontrada.")
        if accion == "eliminar":
            sesion.delete(actividad)
            return
        titulo = texto(datos.get("titulo"), "Título", 150)
        descripcion = texto(datos.get("descripcion"), "Descripción", 2000, False)
        responsable = texto(datos.get("responsable"), "Responsable", 150, False)
        inicio, fin = leer_fecha(datos.get("inicio")), leer_fecha(datos.get("fin"))
        if fin <= inicio:
            raise ValueError("La hora final debe ser posterior a la inicial.")
        consulta = select(ActividadModelo.id).where(ActividadModelo.evento_id == evento_id,
            ActividadModelo.inicio < fin, ActividadModelo.fin > inicio)
        if actividad is not None:
            consulta = consulta.where(ActividadModelo.id != actividad.id)
        if sesion.scalar(consulta.limit(1)) is not None:
            raise ValueError("Ese horario se cruza con otra actividad. Ajusta la hora de inicio o fin.")
        if actividad is None:
            actividad = ActividadModelo(evento_id=evento_id)
            sesion.add(actividad)
        actividad.titulo, actividad.descripcion = titulo, descripcion or None
        actividad.responsable = responsable or None
        actividad.inicio, actividad.fin = inicio, fin
