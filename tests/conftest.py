import os

# Debe configurarse antes de importar app.web durante la colección.
os.environ.setdefault("SECRET_KEY", "clave-efimera-solo-para-pruebas")
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://pruebas:pruebas@localhost/enagenda_test")

import pytest


@pytest.fixture(autouse=True)
def configurar_token_metricas(monkeypatch):
    monkeypatch.setenv("ENAGENDA_METRICS_TOKEN", "token-local-para-pruebas-2026")
    import app.web as web
    web.repositorio._invitaciones.clear()
    web.invitaciones_consultadas_total = 0
