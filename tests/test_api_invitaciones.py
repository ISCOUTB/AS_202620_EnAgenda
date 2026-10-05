import pytest

import app.web as web
from app.web import app


@pytest.fixture
def cliente():
    app.config["TESTING"] = True
    web.invitaciones_consultadas_total = 0
    return app.test_client()


def obtener_token(cliente):
    """Crea una invitación de prueba y devuelve su token."""
    respuesta = cliente.post(
        "/",
        data={
            "destinatario": "Invitado de prueba",
            "fecha_limite": "2099-12-31",
            "hora": "11",
            "minuto": "30",
            "periodo": "PM",
        },
        follow_redirects=False,
    )

    assert respuesta.status_code == 302
    assert respuesta.location is not None

    token = respuesta.location.rsplit("/", 1)[-1]

    return token


def test_get_invitacion_devuelve_datos_del_contrato(cliente):
    token = obtener_token(cliente)

    respuesta = cliente.get(
        f"/api/v1/invitaciones/{token}"
    )

    assert respuesta.status_code == 200

    datos = respuesta.get_json()

    assert datos["token"] == token
    assert "destinatario" in datos
    assert "estado" in datos
    assert "fecha_limite_respuesta" in datos


def test_post_invitacion_confirma_asistencia(cliente):
    token = obtener_token(cliente)

    respuesta = cliente.post(
        f"/api/v1/invitaciones/{token}",
        json={
            "estado": "confirmado"
        },
    )

    assert respuesta.status_code == 200

    datos = respuesta.get_json()

    assert datos["token"] == token
    assert datos["estado"] == "Confirmado"


def test_token_inexistente_devuelve_404(cliente):
    respuesta = cliente.post(
        "/api/v1/invitaciones/token-inexistente",
        json={
            "estado": "confirmado"
        },
    )

    assert respuesta.status_code == 404

    datos = respuesta.get_json()

    assert datos == {
        "error": "Invitación no encontrada."
    }


def test_metricas_aumentan_al_consultar_invitacion(cliente):
    respuesta_inicial = cliente.get("/metrics")

    assert respuesta_inicial.status_code == 200

    metricas_iniciales = respuesta_inicial.get_json()

    assert metricas_iniciales["metric"] == (
        "enagenda_invitaciones_consultadas_total"
    )

    assert metricas_iniciales["value"] == 0

    token = obtener_token(cliente)

    respuesta = cliente.get(
        f"/api/v1/invitaciones/{token}"
    )

    assert respuesta.status_code == 200

    respuesta_final = cliente.get("/metrics")

    assert respuesta_final.status_code == 200

    metricas_finales = respuesta_final.get_json()

    assert metricas_finales["metric"] == (
        "enagenda_invitaciones_consultadas_total"
    )

    assert metricas_finales["value"] == 1