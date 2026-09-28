from app.web import app


def test_health_devuelve_estado_ok():
    cliente = app.test_client()

    respuesta = cliente.get("/health")

    assert respuesta.status_code == 200
    assert respuesta.get_json() == {
        "service": "enagenda-api",
        "status": "ok",
    }


def test_metrics_expone_metricas_http():
    cliente = app.test_client()

    cliente.get("/health")
    respuesta = cliente.get("/metrics")
    datos = respuesta.get_json()

    assert respuesta.status_code == 200
    assert "http_requests_total" in datos
    assert datos["http_requests_total"] >= 1
    assert "http_requests_by_path" in datos
    assert "http_responses_by_status" in datos
    assert "/health" in datos["http_requests_by_path"]