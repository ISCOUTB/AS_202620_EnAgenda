import pytest

from app.web import app


@pytest.fixture
def cliente():
    app.config["TESTING"] = True
    return app.test_client()


def obtener_token(cliente):
    respuesta = cliente.get("/")

    assert respuesta.status_code in (200, 302)

    token = respuesta.location.rsplit("/", 1)[-1]

    assert token

    return token


def test_get_invitacion_devuelve_datos_del_contrato(cliente):
    token = obtener_token(cliente)

    respuesta = cliente.get(f"/api/v1/invitaciones/{token}")

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
        json={"estado": "confirmado"},
    )

    assert respuesta.status_code == 200

    datos = respuesta.get_json()

    assert datos["token"] == token
    assert datos["estado"] == "Confirmado"


def test_token_inexistente_devuelve_404(cliente):
    respuesta = cliente.post(
        "/api/v1/invitaciones/token-inexistente",
        json={"estado": "confirmado"},
    )

    assert respuesta.status_code == 404

    datos = respuesta.get_json()

    assert datos == {
        "error": "Invitación no encontrada."
    }
