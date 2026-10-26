"""Regresiones de atomicidad; SQLite no acredita bloqueos de PostgreSQL."""
from datetime import datetime, timedelta, timezone
from importlib import import_module

import pytest
from sqlalchemy import create_engine, event, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.usuarios.infraestructura.modelo_usuario import Base, UsuarioModelo
from src.eventos.infraestructura.modelo_evento import EventoModelo
from src.invitaciones.infraestructura.modelo_invitacion import InvitacionModelo
from src.invitaciones.infraestructura.repositorio_invitaciones_postgres import RepositorioInvitacionesPostgres


@pytest.fixture
def base_prueba(monkeypatch):
    engine = create_engine('sqlite://', poolclass=StaticPool)
    @event.listens_for(engine, 'connect')
    def activar_fk(conexion, _):
        conexion.execute('PRAGMA foreign_keys=ON')
    Base.metadata.create_all(engine)
    fabrica = sessionmaker(bind=engine, expire_on_commit=False)
    modulo = import_module('src.invitaciones.aplicacion.agregar_invitados')
    monkeypatch.setattr(modulo, 'SessionLocal', fabrica)
    with fabrica() as sesion:
        usuario = UsuarioModelo(nombre='Organizador', correo='org@example.com', contrasena_hash='solo-prueba')
        sesion.add(usuario)
        sesion.flush()
        evento = EventoModelo(usuario_id=usuario.id, titulo='Evento', ubicacion='Cartagena', fecha_evento=datetime.now(timezone.utc)+timedelta(days=7), fecha_limite_confirmacion=datetime.now(timezone.utc)+timedelta(days=6))
        sesion.add(evento)
        sesion.commit()
        ids = evento.id, usuario.id
    yield modulo, fabrica, ids
    engine.dispose()


def invitados(n):
    return [{'nombre': f'Invitado {i}', 'correo': f'inv{i}@example.com'} for i in range(n)]


def cantidad(fabrica):
    with fabrica() as s:
        return s.scalar(select(func.count(InvitacionModelo.id)))


def test_lote_invalido_no_deja_altas_parciales(base_prueba):
    modulo, fabrica, ids = base_prueba
    with pytest.raises(ValueError):
        modulo.agregar_invitados(*ids, invitados(1)+[{'nombre': 'Mal', 'correo': 'invalido'}])
    assert cantidad(fabrica) == 0


def test_error_despues_del_primer_flush_revierte_todo(base_prueba, monkeypatch):
    modulo, fabrica, ids = base_prueba
    original = RepositorioInvitacionesPostgres.guardar
    llamadas = 0
    def fallar(self, invitacion):
        nonlocal llamadas
        llamadas += 1
        if llamadas == 2:
            raise RuntimeError('Fallo de persistencia simulado')
        return original(self, invitacion)
    monkeypatch.setattr(RepositorioInvitacionesPostgres, 'guardar', fallar)
    with pytest.raises(RuntimeError):
        modulo.agregar_invitados(*ids, invitados(2))
    assert llamadas == 2
    assert cantidad(fabrica) == 0


def test_limite_y_reintento_duplicado_no_crean_filas(base_prueba):
    modulo, fabrica, ids = base_prueba
    modulo.agregar_invitados(*ids, invitados(30))
    with pytest.raises(ValueError):
        modulo.agregar_invitados(*ids, invitados(1))
    assert cantidad(fabrica) == 30


def test_reintento_correo_existente_no_duplica(base_prueba):
    modulo, fabrica, ids = base_prueba
    modulo.agregar_invitados(*ids, invitados(1))
    with pytest.raises(ValueError, match='ya está registrado'):
        modulo.agregar_invitados(*ids, invitados(1))
    assert cantidad(fabrica) == 1


def test_otro_propietario_no_puede_agregar(base_prueba):
    modulo, fabrica, (evento, usuario) = base_prueba
    with pytest.raises(ValueError, match='no te pertenece'):
        modulo.agregar_invitados(evento, usuario+1, invitados(1))
    assert cantidad(fabrica) == 0


def test_lote_heredado_valida_antes_de_guardar():
    import app.web as web
    cliente = web.app.test_client()
    from tests.test_api_invitaciones import ExtractorCSRF
    extractor = ExtractorCSRF()
    extractor.feed(cliente.get('/login').get_data(as_text=True))
    respuesta = cliente.post('/crear-invitaciones', data={'csrf_token': extractor.token, 'fecha_limite': '2099-12-31', 'hora': '11', 'minuto': '30', 'periodo': 'PM', 'cantidad_invitados': '2', 'nombre_1': 'Ana', 'correo_1': 'ana@example.com', 'nombre_2': '', 'correo_2': ''})
    assert respuesta.status_code == 400
    assert web.repositorio._invitaciones == {}


def test_respuesta_repetida_y_consulta_sin_cache():
    import app.web as web
    token = web.gestionar_invitacion.crear_invitacion('Ana', datetime.now()+timedelta(days=1)).token
    cliente = web.app.test_client()
    for _ in range(2):
        respuesta = cliente.post(f'/api/v1/invitaciones/{token}', json={'estado': 'confirmado'})
        assert respuesta.status_code == 200
        assert respuesta.get_json()['estado'] == 'Confirmado'
    consulta = cliente.get(f'/api/v1/invitaciones/{token}')
    assert consulta.get_json()['estado'] == 'Confirmado'
    assert consulta.headers['Cache-Control'] == 'no-store'


def test_respuesta_tardia_no_cambia_estado():
    import app.web as web
    invitacion = web.gestionar_invitacion.crear_invitacion('Ana', datetime.now()-timedelta(seconds=1))
    respuesta = web.app.test_client().post(f'/api/v1/invitaciones/{invitacion.token}', json={'estado': 'confirmado'})
    assert respuesta.status_code == 404
    assert invitacion.estado.value == 'Pendiente'
