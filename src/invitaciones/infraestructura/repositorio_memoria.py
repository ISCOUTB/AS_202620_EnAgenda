from src.invitaciones.dominio.invitaciones import Invitacion


class RepositorioInvitacionesMemoria:
    def __init__(self):
        self._invitaciones = {}

    def guardar(self, invitacion: Invitacion) -> None:
        self._invitaciones[invitacion.token] = invitacion

    def buscar_por_token(self, token: str) -> Invitacion | None:
        return self._invitaciones.get(token)