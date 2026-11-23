"""Cierre manual de eventos, sin eliminar invitados ni respuestas."""
from sqlalchemy import select
from src.compartido.infraestructura.base_datos import SessionLocal
from src.usuarios.infraestructura.modelo_usuario import UsuarioModelo
from src.eventos.infraestructura.modelo_evento import EventoModelo


def cerrar_evento(evento_id, usuario_id, estado):
    if estado not in ("finalizado", "cancelado"):
        raise ValueError("Selecciona un estado de cierre válido.")
    with SessionLocal() as sesion:
        # Mismo orden de bloqueo que crear_evento: usuario antes del evento.
        usuario = sesion.scalar(select(UsuarioModelo).where(
            UsuarioModelo.id == usuario_id, UsuarioModelo.activo.is_(True)
        ).with_for_update())
        if usuario is None:
            raise ValueError("La cuenta no está disponible.")
        evento = sesion.scalar(select(EventoModelo).where(
            EventoModelo.id == evento_id, EventoModelo.usuario_id == usuario_id
        ).with_for_update())
        if evento is None:
            raise LookupError("Evento no encontrado.")
        if evento.estado in ("finalizado", "cancelado") and evento.estado != estado:
            raise ValueError("El evento ya está cerrado; su estado se conserva en el historial.")
        evento.estado = estado
        sesion.commit()
