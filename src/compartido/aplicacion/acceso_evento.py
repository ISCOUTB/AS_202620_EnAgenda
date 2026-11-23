"""Acceso a un evento propio y bloqueo común para sus escrituras."""
from sqlalchemy import select
from src.eventos.infraestructura.modelo_evento import EventoModelo
from src.usuarios.infraestructura.modelo_usuario import UsuarioModelo


def obtener_evento(sesion, evento_id, usuario_id, escritura=False):
    consulta = select(EventoModelo).join(UsuarioModelo).where(
        EventoModelo.id == evento_id,
        EventoModelo.usuario_id == usuario_id,
        UsuarioModelo.activo.is_(True),
    )
    if escritura:
        consulta = consulta.with_for_update(of=EventoModelo)
    evento = sesion.scalar(consulta)
    if evento is None:
        raise LookupError("Evento no encontrado.")
    if escritura and evento.estado in ("finalizado", "cancelado"):
        raise ValueError("El evento está cerrado. Solo puedes consultar sus datos.")
    return evento


def datos_evento(evento):
    return {"id": evento.id, "titulo": evento.titulo, "estado": evento.estado,
            "cerrado": evento.estado in ("finalizado", "cancelado"), "fecha_evento": evento.fecha_evento}


def texto(valor, nombre, maximo, obligatorio=True):
    valor = (valor or "").strip()
    if (obligatorio and not valor) or len(valor) > maximo:
        raise ValueError(f"{nombre}: escribe entre {1 if obligatorio else 0} y {maximo} caracteres.")
    return valor


def identificador(valor):
    valor = str(valor or "")
    if not valor.isascii() or not valor.isdecimal() or len(valor) > 10 or not 1 <= int(valor) <= 2147483647:
        raise ValueError("Identificador no válido.")
    return int(valor)
