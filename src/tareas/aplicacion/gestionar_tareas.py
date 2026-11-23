from sqlalchemy import select

from src.compartido.infraestructura.base_datos import SessionLocal
from src.tareas.infraestructura.modelo_tarea import TareaModelo


from src.compartido.aplicacion.acceso_evento import obtener_evento


def _consultar_evento(sesion, evento_id, usuario_id, bloquear=False):
    return obtener_evento(sesion, evento_id, usuario_id, escritura=bloquear)


def _validar_contenido(titulo, descripcion):
    titulo = titulo.strip()
    descripcion = descripcion.strip()

    if not titulo:
        raise ValueError("Escribe el título de la tarea.")

    if len(titulo) > 150:
        raise ValueError("El título admite máximo 150 caracteres.")

    if len(descripcion) > 2000:
        raise ValueError("La descripción admite máximo 2000 caracteres.")

    return titulo, descripcion or None


def consultar_tareas(evento_id, usuario_id):
    with SessionLocal() as sesion:
        evento = _consultar_evento(
            sesion, evento_id, usuario_id
        )

        modelos = sesion.scalars(
            select(TareaModelo)
            .where(TareaModelo.evento_id == evento_id)
            .order_by(
                TareaModelo.completada.asc(),
                TareaModelo.id.desc(),
            )
        ).all()

        tareas = [
            {
                "id": tarea.id,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion,
                "completada": tarea.completada,
            }
            for tarea in modelos
        ]

        return {
            "evento": {
                "id": evento.id,
                "titulo": evento.titulo,
                "estado": evento.estado,
                "cerrado": evento.estado in ("finalizado", "cancelado"),
            },
            "tareas": tareas,
            "total": len(tareas),
            "completadas": sum(
                tarea["completada"] for tarea in tareas
            ),
        }


def modificar_tareas(
    evento_id,
    usuario_id,
    accion,
    tarea_id=None,
    titulo="",
    descripcion="",
    estado="",
):
    acciones_validas = {
        "crear", "editar", "estado", "eliminar"
    }

    if accion not in acciones_validas:
        raise ValueError("Acción no válida.")

    with SessionLocal.begin() as sesion:
        _consultar_evento(
            sesion,
            evento_id,
            usuario_id,
            bloquear=True,
        )

        if accion == "crear":
            titulo, descripcion = _validar_contenido(
                titulo, descripcion
            )

            sesion.add(
                TareaModelo(
                    evento_id=evento_id,
                    titulo=titulo,
                    descripcion=descripcion,
                    completada=False,
                )
            )
            return

        tarea = sesion.scalar(
            select(TareaModelo)
            .where(
                TareaModelo.id == tarea_id,
                TareaModelo.evento_id == evento_id,
            )
            .with_for_update()
        )

        if tarea is None:
            raise LookupError("Tarea no encontrada.")

        if accion == "editar":
            tarea.titulo, tarea.descripcion = _validar_contenido(
                titulo, descripcion
            )

        elif accion == "estado":
            if estado not in {"pendiente", "completada"}:
                raise ValueError("Estado no válido.")

            tarea.completada = estado == "completada"

        elif accion == "eliminar":
            sesion.delete(tarea)