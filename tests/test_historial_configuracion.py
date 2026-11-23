"""Flujos HTTP con CSRF real y base aislada: no usan los datos del usuario."""
from datetime import datetime, timedelta, timezone
from importlib import import_module
from html.parser import HTMLParser

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from werkzeug.security import generate_password_hash, check_password_hash

import app.web as web
from src.usuarios.infraestructura.modelo_usuario import Base, UsuarioModelo
from src.eventos.infraestructura.modelo_evento import EventoModelo
from src.invitaciones.infraestructura.modelo_invitacion import InvitacionModelo


class TokenCSRF(HTMLParser):
    token = None
    def handle_starttag(self, tag, attrs):
        atributos = dict(attrs)
        if tag == 'input' and atributos.get('name') == 'csrf_token':
            self.token = atributos['value']


@pytest.fixture
def cuenta(monkeypatch):
    engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    fabrica = sessionmaker(bind=engine, expire_on_commit=False)
    monkeypatch.setattr(web, 'SessionLocal', fabrica)
    for nombre in ('src.usuarios.aplicacion.configurar_cuenta', 'src.usuarios.aplicacion.autenticar_usuario', 'src.eventos.aplicacion.cerrar_evento', 'src.eventos.aplicacion.crear_evento', 'src.invitaciones.aplicacion.agregar_invitados'):
        monkeypatch.setattr(import_module(nombre), 'SessionLocal', fabrica)
    monkeypatch.setitem(web.app.config, 'TESTING', True)
    with fabrica() as s:
        s.add_all([UsuarioModelo(id=1, nombre='Ana', correo='ana@example.com', contrasena_hash=generate_password_hash('Clave1234')), UsuarioModelo(id=2, nombre='Otro', correo='otro@example.com', contrasena_hash=generate_password_hash('Clave5678'))])
        s.flush()
        for i in range(1, 5):
            s.add(EventoModelo(id=i, usuario_id=1, titulo=f'Celebración {i}', ubicacion='Cartagena', fecha_evento=datetime.now(timezone.utc)+timedelta(days=10), fecha_limite_confirmacion=datetime.now(timezone.utc)+timedelta(days=5)))
        s.add(EventoModelo(id=5, usuario_id=2, titulo='Privado de otro', ubicacion='Cartagena', estado='finalizado', fecha_evento=datetime.now(timezone.utc), fecha_limite_confirmacion=datetime.now(timezone.utc)))
        s.flush()
        s.add(InvitacionModelo(evento_id=1, nombre='Invitada', correo='inv@example.com', token='invitacion-prueba', estado='confirmado'))
        s.commit()
    cliente = web.app.test_client()
    with cliente.session_transaction() as sesion:
        sesion['usuario_id'] = 1
    yield cliente, fabrica
    engine.dispose()


def enviar(cliente, ruta, datos):
    pagina = cliente.get('/configuracion')
    parser = TokenCSRF()
    parser.feed(pagina.get_data(as_text=True))
    return cliente.post(ruta, data={**datos, 'csrf_token': parser.token})


def test_historial_cierra_conserva_y_libera_cupo(cuenta):
    cliente, fabrica = cuenta
    assert 'Celebración 1' in cliente.get('/panel').text
    respuesta = enviar(cliente, '/eventos/1/cerrar', {'estado': 'finalizado'})
    assert respuesta.status_code == 302
    historial = cliente.get('/historial')
    assert 'Celebración 1' in historial.text
    assert 'Privado de otro' not in historial.text
    assert 'Celebración 1' not in cliente.get('/panel').text
    with fabrica() as s:
        assert s.get(EventoModelo, 1).estado == 'finalizado'
        assert s.scalar(select(InvitacionModelo)).estado == 'confirmado'
        from src.eventos.infraestructura.repositorio_eventos import RepositorioEventos
        assert RepositorioEventos(s).contar_activos(1) == 3
    from src.eventos.aplicacion.crear_evento import crear_evento
    nuevo_evento = crear_evento(1, 'Nuevo cupo', '', 'Cartagena', datetime.now(timezone.utc)+timedelta(days=20), datetime.now(timezone.utc)+timedelta(days=19))
    assert nuevo_evento['usuario_id'] == 1
    pagina = cliente.get('/eventos/1/invitados')
    assert 'Invitada' in pagina.text
    assert 'name="nombre[]"' not in pagina.text
    # Nuevo cliente/sesión: el historial no depende de la sesión anterior.
    nuevo = web.app.test_client()
    with nuevo.session_transaction() as sesion:
        sesion['usuario_id'] = 1
    assert 'Celebración 1' in nuevo.get('/historial').text


def test_cancelacion_y_filtro(cuenta):
    cliente, _ = cuenta
    enviar(cliente, '/eventos/1/cerrar', {'estado': 'cancelado'})
    assert 'Celebración 1' in cliente.get('/historial?estado=cancelado').text
    assert 'Celebración 1' not in cliente.get('/historial?estado=finalizado').text
    assert cliente.get('/historial?estado=incorrecto').status_code == 400


def test_cierre_ajeno_y_estado_invalido(cuenta):
    cliente, fabrica = cuenta
    assert enviar(cliente, '/eventos/5/cerrar', {'estado': 'cancelado'}).status_code == 404
    enviar(cliente, '/eventos/1/cerrar', {'estado': 'incorrecto'})
    with fabrica() as s:
        assert s.get(EventoModelo, 1).estado == 'borrador'
    assert cliente.get('/eventos/5').status_code == 404


def test_no_reabre_ni_cambia_evento_ya_cerrado(cuenta):
    cliente, fabrica = cuenta
    enviar(cliente, '/eventos/1/cerrar', {'estado': 'finalizado'})
    enviar(cliente, '/eventos/1/cerrar', {'estado': 'cancelado'})
    with fabrica() as s:
        assert s.get(EventoModelo, 1).estado == 'finalizado'
    # Un POST directo tampoco puede agregar invitados al evento cerrado.
    from src.invitaciones.aplicacion.agregar_invitados import agregar_invitados
    with pytest.raises(ValueError, match='evento cerrado'):
        agregar_invitados(1, 1, [{'nombre': 'Nueva', 'correo': 'nueva@example.com'}])
    # POST de invitado cerrado conserva la respuesta original.
    respuesta = enviar(cliente, '/eventos/invitacion/invitacion-prueba', {'estado': 'no_asistire'})
    assert 'El plazo para responder ha finalizado' in respuesta.text
    with fabrica() as s:
        assert s.scalar(select(InvitacionModelo)).estado == 'confirmado'


def test_perfil_persiste_y_login_con_nuevo_correo(cuenta):
    cliente, fabrica = cuenta
    assert enviar(cliente, '/configuracion', {'accion': 'perfil', 'nombre': 'Ana María', 'correo': ' NUEVO@EXAMPLE.COM ', 'contrasena_actual': 'Clave1234'}).status_code == 302
    with fabrica() as s:
        u = s.get(UsuarioModelo, 1)
        assert (u.nombre, u.correo) == ('Ana María', 'nuevo@example.com')
    from src.usuarios.aplicacion.autenticar_usuario import autenticar_usuario
    assert autenticar_usuario('nuevo@example.com', 'Clave1234')['id'] == 1
    assert autenticar_usuario('ana@example.com', 'Clave1234') is None


@pytest.mark.parametrize('cambios', [
    {'correo': 'otro@example.com'}, {'correo': 'invalido'}, {'nombre': ''}, {'contrasena_actual': 'mala'}
])
def test_perfil_invalido_no_escribe(cuenta, cambios):
    cliente, fabrica = cuenta
    datos = {'accion': 'perfil', 'nombre': 'Ana', 'correo': 'ana@example.com', 'contrasena_actual': 'Clave1234', **cambios}
    assert enviar(cliente, '/configuracion', datos).status_code == 400
    with fabrica() as s:
        assert s.get(UsuarioModelo, 1).correo == 'ana@example.com'
        assert s.get(UsuarioModelo, 1).nombre == 'Ana'


def test_contrasena_valida_reemplaza_hash(cuenta):
    cliente, fabrica = cuenta
    assert enviar(cliente, '/configuracion', {'accion': 'contrasena', 'contrasena_actual': 'Clave1234', 'nueva_contrasena': 'NuevaClave567', 'confirmar_contrasena': 'NuevaClave567'}).status_code == 302
    with fabrica() as s:
        clave = s.get(UsuarioModelo, 1).contrasena_hash
        assert check_password_hash(clave, 'NuevaClave567')
        assert not check_password_hash(clave, 'Clave1234')


@pytest.mark.parametrize('nueva,confirmacion', [('corta','corta'), ('Nueva1234','otra')])
def test_clave_invalida_conserva_hash(cuenta, nueva, confirmacion):
    cliente, fabrica = cuenta
    assert enviar(cliente, '/configuracion', {'accion':'contrasena', 'contrasena_actual':'Clave1234', 'nueva_contrasena':nueva, 'confirmar_contrasena':confirmacion}).status_code == 400
    with fabrica() as s:
        assert check_password_hash(s.get(UsuarioModelo, 1).contrasena_hash, 'Clave1234')


def test_tema_por_cuenta_persistente(cuenta):
    cliente, fabrica = cuenta
    assert enviar(cliente, '/configuracion', {'accion': 'apariencia', 'tema': 'verde'}).status_code == 302
    assert '--accent: #247451' in cliente.get('/panel').text
    assert '--accent: #247451' in cliente.get('/eventos/1').text
    with fabrica() as s:
        assert s.get(UsuarioModelo, 1).tema == 'verde'
        assert s.get(UsuarioModelo, 2).tema == 'violeta'
    assert enviar(cliente, '/configuracion', {'accion': 'apariencia', 'tema': '<script>'}).status_code == 400


def test_login_csrf_y_no_store(cuenta):
    cliente, fabrica = cuenta
    assert cliente.post('/eventos/1/cerrar', data={'estado':'cancelado'}).status_code == 400
    assert cliente.post('/configuracion', data={'accion':'apariencia','tema':'rosa'}).status_code == 400
    assert cliente.get('/historial').headers['Cache-Control'] == 'no-store'
    anonimo = web.app.test_client()
    assert anonimo.get('/historial').status_code == 302
    assert anonimo.get('/configuracion').status_code == 302
    with fabrica() as s:
        s.get(UsuarioModelo, 1).activo = False
        s.commit()
    assert cliente.get('/configuracion').status_code == 302


def test_migracion_conserva_usuarios_existentes(tmp_path, monkeypatch):
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import text, inspect
    import src.compartido.infraestructura.base_datos as base_datos
    url = 'sqlite:///' + str(tmp_path / 'migracion.db')
    monkeypatch.setattr(base_datos, 'DATABASE_URL', url)
    configuracion = Config('alembic.ini')
    command.upgrade(configuracion, 'b303d9dbf5e5')
    motor = create_engine(url)
    with motor.begin() as conexion:
        conexion.execute(text("INSERT INTO usuarios (nombre, correo, contrasena_hash, activo, fecha_registro) VALUES ('Existente', 'existente@example.com', 'hash-previo', 1, CURRENT_TIMESTAMP)"))
    command.upgrade(configuracion, 'head')
    with motor.connect() as conexion:
        assert conexion.execute(text('SELECT nombre, tema FROM usuarios')).one() == ('Existente', 'violeta')
    command.downgrade(configuracion, 'b303d9dbf5e5')
    assert 'tema' not in {c['name'] for c in inspect(motor).get_columns('usuarios')}
    with motor.connect() as conexion:
        assert conexion.execute(text('SELECT nombre FROM usuarios')).scalar_one() == 'Existente'
    command.upgrade(configuracion, 'head')
    motor.dispose()
