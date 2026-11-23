"""Flujos de módulos con CSRF activo, dinero exacto y aislamiento por evento."""
from decimal import Decimal
from importlib import import_module

import pytest
from sqlalchemy import select
from tests.test_historial_configuracion import cuenta, enviar
from src.agenda.infraestructura.modelo_actividad import ActividadModelo
from src.presupuesto.infraestructura.modelos_presupuesto import GastoModelo, PresupuestoModelo
from src.tareas.infraestructura.modelo_tarea import TareaModelo
from src.usuarios.infraestructura.modelo_usuario import UsuarioModelo
import app.web as web


@pytest.fixture
def operacion(cuenta, monkeypatch):
    cliente, fabrica = cuenta
    for nombre in ('src.agenda.aplicacion.gestionar_agenda', 'src.presupuesto.aplicacion.gestionar_presupuesto', 'src.tareas.aplicacion.gestionar_tareas'):
        monkeypatch.setattr(import_module(nombre), 'SessionLocal', fabrica)
    return cliente, fabrica


def actividad(**cambios):
    return {'accion': 'crear', 'titulo': 'Recepción', 'inicio': '2026-12-25T09:00', 'fin': '2026-12-25T10:00', 'responsable': 'Ana', 'descripcion': 'Entrada al salón', **cambios}


def gasto(**cambios):
    return {'accion':'crear', 'concepto':'Lugar', 'categoria':'Logística', 'valor':'1000.10', 'notas':'Reserva', **cambios}


def test_agenda_crud_y_zona_horaria(operacion):
    cliente, fabrica = operacion
    ruta = '/eventos/1/agenda'
    assert enviar(cliente,ruta,actividad()).status_code == 303
    with fabrica() as s:
        a = s.scalar(select(ActividadModelo))
        assert a.inicio.hour == 14  # 09:00 Cartagena = 14:00 UTC
        id_a = a.id
    pagina = cliente.get(ruta)
    assert pagina.status_code == 200
    assert 'Recepción' in pagina.text and '09:00 AM' in pagina.text
    assert enviar(cliente,ruta,actividad(accion='editar',actividad_id=str(id_a),titulo='Bienvenida')).status_code == 303
    assert 'Bienvenida' in cliente.get(ruta).text
    assert enviar(cliente,ruta,{'accion':'eliminar','actividad_id':str(id_a)}).status_code == 303
    with fabrica() as s:
        assert s.scalar(select(ActividadModelo)) is None


def test_agenda_cruce_rechazado_adyacente_permitida(operacion):
    cliente, fabrica = operacion
    ruta = '/eventos/1/agenda'
    enviar(cliente,ruta,actividad())
    assert enviar(cliente,ruta,actividad(titulo='Cruce',inicio='2026-12-25T09:30',fin='2026-12-25T11:00')).status_code == 400
    assert enviar(cliente,ruta,actividad(titulo='Siguiente',inicio='2026-12-25T10:00',fin='2026-12-25T11:00')).status_code == 303
    with fabrica() as s:
        assert len(s.scalars(select(ActividadModelo)).all()) == 2
    # Una actividad puede conservar sus propias horas al editarse.
    assert enviar(cliente,ruta,actividad(accion='editar',actividad_id='1')).status_code == 303


@pytest.mark.parametrize('cambios',[{'fin':'2026-12-25T08:00'}, {'fin':'2026-12-25T09:00'}, {'inicio':'invalido'}, {'titulo':''}, {'actividad_id':'-1','accion':'editar'}, {'accion':'otra'}])
def test_agenda_datos_invalidos_no_escriben(operacion,cambios):
    cliente,fabrica=operacion
    assert enviar(cliente,'/eventos/1/agenda',actividad(**cambios)).status_code == 400
    with fabrica() as s:
        assert s.scalar(select(ActividadModelo)) is None


def test_presupuesto_totales_decimales_y_pagos(operacion):
    cliente,fabrica=operacion
    ruta='/eventos/1/presupuesto'
    assert enviar(cliente,ruta,{'accion':'limite','limite':'1.00'}).status_code == 303
    assert enviar(cliente,ruta,gasto(valor='0.10')).status_code == 303
    assert enviar(cliente,ruta,gasto(concepto='Comida',valor='0.20')).status_code == 303
    from src.presupuesto.aplicacion.gestionar_presupuesto import consultar_presupuesto
    datos=consultar_presupuesto(1,1)
    assert (datos['total'],datos['saldo']) == (Decimal('0.30'),Decimal('0.70'))
    assert enviar(cliente,ruta,{'accion':'pago','gasto_id':'1','estado':'pagado'}).status_code == 303
    datos=consultar_presupuesto(1,1)
    assert datos['pagado']==Decimal('0.10') and datos['pendiente']==Decimal('0.20')
    assert '$ 0,30 COP' in cliente.get(ruta).text
    # Edición no pierde la marca de pago.
    assert enviar(cliente,ruta,gasto(accion='editar',gasto_id='1',valor='0.40')).status_code == 303
    assert consultar_presupuesto(1,1)['pagado']==Decimal('0.40')
    assert enviar(cliente,ruta,{'accion':'eliminar','gasto_id':'2'}).status_code == 303
    assert consultar_presupuesto(1,1)['total']==Decimal('0.40')


def test_presupuesto_sin_limite_y_sobrecosto(operacion):
    cliente,fabrica=operacion
    ruta='/eventos/1/presupuesto'
    assert cliente.get(ruta).status_code==200
    assert 'Sin definir' in cliente.get(ruta).text
    enviar(cliente,ruta,gasto(valor='15.25'))
    assert enviar(cliente,ruta,{'accion':'limite','limite':'0'}).status_code == 303
    assert 'superan tu presupuesto' in cliente.get(ruta).text


@pytest.mark.parametrize('valor',['NaN','Infinity','1e3','-2','0','1.234','99999999999','1,000.50'])
def test_montos_invalidos_no_crean_gasto(operacion,valor):
    cliente,fabrica=operacion
    assert enviar(cliente,'/eventos/1/presupuesto',gasto(valor=valor)).status_code==400
    with fabrica() as s:
        assert s.scalar(select(GastoModelo)) is None


@pytest.mark.parametrize('modulo',['agenda','presupuesto','tareas'])
def test_modulos_ajenos_cerrados_y_csrf(operacion,modulo):
    cliente,fabrica=operacion
    ruta=f'/eventos/1/{modulo}'
    payload={'agenda':actividad(),'presupuesto':gasto(),'tareas':{'accion':'crear','titulo':'Reservar'}}[modulo]
    assert cliente.post(ruta,data=payload).status_code==400
    assert cliente.get(f'/eventos/5/{modulo}').status_code==404
    assert enviar(cliente,f'/eventos/5/{modulo}',payload).status_code==404
    enviar(cliente,'/eventos/1/cerrar',{'estado':'finalizado'})
    assert cliente.get(ruta).status_code==200
    assert enviar(cliente,ruta,payload).status_code==400
    anonimo=web.app.test_client()
    assert anonimo.get(ruta).status_code==302


def test_no_mueve_registros_entre_eventos(operacion):
    cliente,fabrica=operacion
    enviar(cliente,'/eventos/1/agenda',actividad())
    enviar(cliente,'/eventos/1/presupuesto',gasto())
    assert enviar(cliente,'/eventos/2/agenda',actividad(accion='editar',actividad_id='1')).status_code==404
    assert enviar(cliente,'/eventos/2/presupuesto',gasto(accion='editar',gasto_id='1')).status_code==404
    from src.agenda.aplicacion.gestionar_agenda import consultar_agenda
    assert consultar_agenda(2,1)['actividades'] == []


def test_tareas_crud_y_persistencia(operacion):
    cliente,fabrica=operacion
    ruta='/eventos/1/tareas'
    assert enviar(cliente,ruta,{'accion':'crear','titulo':'Reservar','descripcion':'Llamar al salón'}).status_code==303
    assert enviar(cliente,ruta,{'accion':'estado','tarea_id':'1','estado':'completada'}).status_code==303
    assert enviar(cliente,ruta,{'accion':'editar','tarea_id':'1','titulo':'Reserva lista','descripcion':''}).status_code==303
    with fabrica() as s:
        t=s.scalar(select(TareaModelo))
        assert t.completada and t.titulo=='Reserva lista'
    assert enviar(cliente,ruta,{'accion':'eliminar','tarea_id':'1'}).status_code==303
    assert 'Reserva lista' not in cliente.get(ruta).text


@pytest.mark.parametrize('tema',['azul','terracota','vino','verde'])
def test_paleta_completa_en_todas_las_areas(operacion,tema):
    cliente,fabrica=operacion
    from src.usuarios.aplicacion.temas import PALETAS
    assert enviar(cliente,'/configuracion',{'accion':'apariencia','tema':tema}).status_code==302
    for ruta in ('/panel','/configuracion','/historial','/eventos/1','/eventos/1/tareas','/eventos/1/agenda','/eventos/1/presupuesto'):
        html=cliente.get(ruta).text
        assert '--navy: '+PALETAS[tema]['navy'] in html
        assert '--accent: '+PALETAS[tema]['accent'] in html
    enviar(cliente,'/logout',{})
    assert '--navy: '+PALETAS[tema]['navy'] in cliente.get('/login').text
    with fabrica() as s:
        assert s.get(UsuarioModelo,1).tema==tema
        assert s.get(UsuarioModelo,2).tema=='azul'


def test_anonimo_azul_y_escape_html(operacion):
    cliente,_=operacion
    assert '--navy: #071c2c' in web.app.test_client().get('/login').text
    enviar(cliente,'/eventos/1/agenda',actividad(titulo='<script>alert(1)</script>'))
    html=cliente.get('/eventos/1/agenda').text
    assert '<script>alert(1)</script>' not in html
    assert '&lt;script&gt;' in html


def test_migracion_desde_merge_conserva_tareas_y_mapea_temas(tmp_path,monkeypatch):
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import create_engine, text, inspect
    import src.compartido.infraestructura.base_datos as base_datos
    url='sqlite:///'+str(tmp_path/'evolucion.db')
    monkeypatch.setattr(base_datos,'DATABASE_URL',url)
    cfg=Config('alembic.ini')
    command.upgrade(cfg,'7d297b6ad7b3')
    engine=create_engine(url)
    with engine.begin() as c:
        for i,tema in enumerate(('violeta','rosa','verde','azul'),1):
            c.execute(text("INSERT INTO usuarios (id,nombre,correo,contrasena_hash,activo,fecha_registro,tema) VALUES (:i,'Existente',:correo,'hash',1,CURRENT_TIMESTAMP,:tema)"), {'i':i,'correo':f'{i}@example.com','tema':tema})
        c.execute(text("INSERT INTO eventos (id,usuario_id,titulo,ubicacion,fecha_evento,fecha_limite_confirmacion,estado,fecha_creacion) VALUES (1,1,'Evento previo','Cartagena',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,'borrador',CURRENT_TIMESTAMP)"))
        c.execute(text("INSERT INTO tareas (evento_id,titulo,completada) VALUES (1,'Tarea previa',0)"))
        c.execute(text("INSERT INTO invitaciones (evento_id,nombre,correo,token,estado,fecha_creacion) VALUES (1,'Invitada','inv@example.com','token-previo','confirmado',CURRENT_TIMESTAMP)"))
    command.upgrade(cfg,'head')
    with engine.connect() as c:
        assert c.execute(text('SELECT tema FROM usuarios ORDER BY id')).scalars().all()==['azul','vino','verde','azul']
        assert c.execute(text('SELECT titulo FROM tareas')).scalar_one()=='Tarea previa'
        assert c.execute(text('SELECT token FROM invitaciones')).scalar_one()=='token-previo'
    assert {'gastos','presupuestos','actividades_agenda'} <= set(inspect(engine).get_table_names())
    command.downgrade(cfg,'7d297b6ad7b3')
    with engine.connect() as c:
        assert c.execute(text('SELECT titulo FROM tareas')).scalar_one()=='Tarea previa'
    command.upgrade(cfg,'head')
    engine.dispose()
