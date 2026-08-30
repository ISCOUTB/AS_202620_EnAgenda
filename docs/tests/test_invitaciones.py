from datetime import datetime, timedelta

import pytest

from src.invitaciones.aplicacion.gestionar_invitacion import (
    GestionarInvitacion
)
from src.invitaciones.dominio.invitacion import (
    EstadoInvitacion
)
from src.invitaciones.infraestructura.repositorio_memoria import (
    RepositorioInvitacionesMemoria
)


@pytest.fixture
def servicio():
    repositorio = RepositorioInvitacionesMemoria()
    return GestionarInvitacion(repositorio)


def test_crear_invitacion_genera_token_y_estado_pendiente(servicio):
    ahora = datetime.now()
    limite = ahora + timedelta(days=7)

    invitacion = servicio.crear_invitacion(
        destinatario="Juan",
        fecha_limite_respuesta=limite
    )

    assert invitacion.token
    assert invitacion.destinatario == "Juan"
    assert invitacion.estado == EstadoInvitacion.PENDIENTE


def test_token_valido_permite_consultar_invitacion(servicio):
    ahora = datetime.now()

    invitacion = servicio.crear_invitacion(
        destinatario="Juan",
        fecha_limite_respuesta=ahora + timedelta(days=1)
    )

    resultado = servicio.consultar(
        token=invitacion.token,
        ahora=ahora
    )

    assert resultado.token == invitacion.token
    assert resultado.destinatario == "Juan"


def test_token_inexistente_es_rechazado(servicio):
    ahora = datetime.now()

    with pytest.raises(ValueError, match="Invitación no encontrada"):
        servicio.consultar(
            token="token-inexistente",
            ahora=ahora
        )


def test_invitacion_vencida_bloquea_el_acceso(servicio):
    ahora = datetime.now()

    invitacion = servicio.crear_invitacion(
        destinatario="Juan",
        fecha_limite_respuesta=ahora - timedelta(minutes=1)
    )

    with pytest.raises(ValueError, match="invitación está vencida"):
        servicio.consultar(
            token=invitacion.token,
            ahora=ahora
        )


def test_invitado_puede_cambiar_su_respuesta_mientras_este_vigente(servicio):
    ahora = datetime.now()

    invitacion = servicio.crear_invitacion(
        destinatario="Juan",
        fecha_limite_respuesta=ahora + timedelta(days=1)
    )

    servicio.responder(
        token=invitacion.token,
        estado=EstadoInvitacion.CONFIRMADO,
        ahora=ahora
    )

    assert invitacion.estado == EstadoInvitacion.CONFIRMADO

    servicio.responder(
        token=invitacion.token,
        estado=EstadoInvitacion.NO_ASISTIRE,
        ahora=ahora
    )

    assert invitacion.estado == EstadoInvitacion.NO_ASISTIRE


def test_invitacion_vencida_no_permite_cambiar_respuesta(servicio):
    ahora = datetime.now()

    invitacion = servicio.crear_invitacion(
        destinatario="Juan",
        fecha_limite_respuesta=ahora - timedelta(minutes=1)
    )

    with pytest.raises(ValueError, match="invitación está vencida"):
        servicio.responder(
            token=invitacion.token,
            estado=EstadoInvitacion.CONFIRMADO,
            ahora=ahora
        )