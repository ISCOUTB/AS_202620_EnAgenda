from datetime import datetime

from src.invitaciones.dominio.invitacion import (
    EstadoInvitacion,
    Invitacion
)
from src.invitaciones.infraestructura.repositorio_memoria import (
    RepositorioInvitacionesMemoria
)


class GestionarInvitacion:
    def __init__(self, repositorio: RepositorioInvitacionesMemoria):
        self.repositorio = repositorio

    def crear_invitacion(
        self,
        destinatario: str,
        fecha_limite_respuesta: datetime
    ) -> Invitacion:
        invitacion = Invitacion.crear(
            destinatario=destinatario,
            fecha_limite_respuesta=fecha_limite_respuesta
        )

        self.repositorio.guardar(invitacion)

        return invitacion

    def consultar(
        self,
        token: str,
        ahora: datetime
    ) -> Invitacion:
        invitacion = self.repositorio.buscar_por_token(token)

        if invitacion is None:
            raise ValueError("Invitación no encontrada.")

        if not invitacion.esta_vigente(ahora):
            raise ValueError("La invitación está vencida.")

        return invitacion

    def responder(
        self,
        token: str,
        estado: EstadoInvitacion,
        ahora: datetime
    ) -> Invitacion:
        invitacion = self.consultar(token, ahora)

        invitacion.cambiar_estado(
            nuevo_estado=estado,
            ahora=ahora
        )

        self.repositorio.guardar(invitacion)

        return invitacion