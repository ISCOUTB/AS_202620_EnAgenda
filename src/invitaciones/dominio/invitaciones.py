from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import secrets


class EstadoInvitacion(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADO = "Confirmado"
    NO_ASISTIRE = "No asistiré"


@dataclass
class Invitacion:
    token: str
    destinatario: str
    fecha_limite_respuesta: datetime
    estado: EstadoInvitacion = EstadoInvitacion.PENDIENTE

    @classmethod
    def crear(
        cls,
        destinatario: str,
        fecha_limite_respuesta: datetime
    ) -> "Invitacion":
        token = secrets.token_urlsafe(32)

        return cls(
            token=token,
            destinatario=destinatario,
            fecha_limite_respuesta=fecha_limite_respuesta
        )

    def esta_vigente(self, ahora: datetime) -> bool:
        return ahora <= self.fecha_limite_respuesta

    def cambiar_estado(
        self,
        nuevo_estado: EstadoInvitacion,
        ahora: datetime
    ) -> None:
        if not self.esta_vigente(ahora):
            raise ValueError("La invitación está vencida.")

        if not isinstance(nuevo_estado, EstadoInvitacion):
            raise ValueError("Estado de invitación no válido.")

        self.estado = nuevo_estado