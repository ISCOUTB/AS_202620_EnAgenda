# 5. Vista de Bloques de Construcción

## 5.1 Descomposición del sistema

EnAgenda está organizado como un monolito modular. Los módulos funcionales del sistema se encuentran dentro de `src/`.

Actualmente se identifican los siguientes módulos:

- Eventos.
- Invitaciones.
- Tareas.
- Agenda.
- Presupuesto.
- Panel de seguimiento.
- Compartido.

Estos bloques representan las principales áreas funcionales previstas para EnAgenda. El nivel de implementación puede variar entre los diferentes módulos.

La aplicación cuenta además con una capa de entrada web ubicada en `app/`, implementada con Flask. Esta capa recibe las solicitudes HTTP, renderiza las vistas mediante Jinja2 y conecta la interfaz con los casos de uso de los módulos correspondientes.

En el estado actual del proyecto, el módulo de Invitaciones constituye el corte vertical funcional con mayor nivel de implementación.

El flujo principal implementado puede representarse de la siguiente manera:

```text
Usuario
   ↓
Interfaz web
HTML + CSS + Jinja2
   ↓
app/web.py
Flask
   ↓
GestionarInvitacion
   ↓
Invitacion / EstadoInvitacion
   ↓
RepositorioInvitacionesMemoria
```

## 5.2 Bloque de entrada web

La capa de entrada web se encuentra en:

`app/`

Su archivo principal es:

`app/web.py`

Este bloque tiene como responsabilidades:

- Definir las rutas HTTP de la aplicación.
- Recibir los datos enviados mediante formularios.
- Realizar validaciones relacionadas con la entrada de datos.
- Renderizar las plantillas HTML mediante Jinja2.
- Exponer los endpoints HTTP de la API implementada.
- Delegar las operaciones relacionadas con invitaciones en `GestionarInvitacion`.

Las plantillas utilizadas por la interfaz se encuentran en:

`app/templates/`

Los estilos de la interfaz se encuentran en:

`app/static/css/`

La capa web actúa como punto de entrada al sistema, pero no debe concentrar las reglas principales del dominio ni conocer los detalles internos del mecanismo de persistencia.

## 5.3 Bloque de Invitaciones

El bloque de Invitaciones es el módulo que actualmente cuenta con una implementación funcional identificable en el código.

Se encuentra en:

`src/invitaciones/`

Está organizado en tres partes principales:

- `aplicacion`
- `dominio`
- `infraestructura`

### Aplicación

Ruta principal:

`src/invitaciones/aplicacion/gestionar_invitacion.py`

La capa de aplicación contiene `GestionarInvitacion`.

Su responsabilidad es coordinar los casos de uso relacionados con la gestión de invitaciones, utilizando las reglas definidas por el dominio y el mecanismo de almacenamiento proporcionado por infraestructura.

La capa web delega en este componente operaciones como la creación, consulta y respuesta de las invitaciones.

### Dominio

Ruta:

`src/invitaciones/dominio/invitaciones.py`

El dominio contiene la entidad `Invitacion` y el enumerado `EstadoInvitacion`.

La entidad representa una invitación y maneja información como:

- Token de identificación.
- Destinatario.
- Fecha límite de respuesta.
- Estado de la invitación.

También concentra las reglas relacionadas con la creación de una invitación, la comprobación de su vigencia y la actualización de su estado.

Los estados definidos actualmente son:

- `PENDIENTE`
- `CONFIRMADO`
- `NO_ASISTIRE`

### Infraestructura

Ruta:

`src/invitaciones/infraestructura/repositorio_memoria.py`

Esta capa contiene `RepositorioInvitacionesMemoria`.

Su responsabilidad es almacenar temporalmente las invitaciones y permitir su recuperación mediante el token correspondiente.

La implementación actual utiliza almacenamiento en memoria. Por esta razón, los datos almacenados no sobreviven al reinicio de la aplicación.

Este mecanismo permite mantener separadas las reglas del dominio de los detalles concretos de persistencia y podrá ser sustituido posteriormente por una solución permanente.

## 5.4 Relación entre los bloques

El flujo implementado para la gestión de invitaciones atraviesa los bloques de entrada web, aplicación, dominio e infraestructura.

La relación principal es:

```text
app/web.py
    ↓
GestionarInvitacion
    ↓
Invitacion / EstadoInvitacion
    ↓
RepositorioInvitacionesMemoria
```

`app/web.py` recibe las solicitudes HTTP y delega las operaciones del negocio en `GestionarInvitacion`.

`GestionarInvitacion` coordina los casos de uso y utiliza los elementos del dominio para aplicar las reglas correspondientes.

El dominio representa las invitaciones, sus estados y sus reglas.

`RepositorioInvitacionesMemoria` proporciona el mecanismo actual para guardar y recuperar las invitaciones.

Esta separación permite que la interfaz web y la infraestructura puedan evolucionar sin trasladar sus responsabilidades al dominio.

## 5.5 Correspondencia entre arquitectura y código

La correspondencia actual entre los principales bloques arquitectónicos y el código es:

| Bloque | Responsabilidad | Código |
|---|---|---|
| Entrada web | Recibir solicitudes HTTP, renderizar vistas y delegar casos de uso | `app/web.py` |
| Plantillas web | Representar las pantallas del flujo de invitaciones | `app/templates/` |
| Estilos web | Definir la presentación visual de las vistas | `app/static/css/` |
| Invitaciones - Aplicación | Coordinar los casos de uso de invitaciones | `src/invitaciones/aplicacion/gestionar_invitacion.py` |
| Invitaciones - Dominio | Representar las invitaciones, sus estados y reglas | `src/invitaciones/dominio/invitaciones.py` |
| Invitaciones - Infraestructura | Guardar y recuperar invitaciones temporalmente | `src/invitaciones/infraestructura/repositorio_memoria.py` |

Los demás módulos presentes en `src/` forman parte de la estructura modular prevista para EnAgenda.

No se atribuyen en esta sección responsabilidades de implementación que todavía no estén respaldadas por código funcional.

## 5.6 Relación con C4

La vista de bloques de construcción complementa los diagramas C4 al mostrar con mayor detalle cómo se organiza internamente la implementación actual de EnAgenda.

En el corte vertical del módulo de Invitaciones, la aplicación Flask funciona como punto de entrada web y se comunica con la capa de aplicación mediante `GestionarInvitacion`.

La capa de aplicación utiliza el dominio de Invitaciones y la infraestructura proporciona actualmente un repositorio en memoria.

Por lo tanto, la implementación actual no depende de un contenedor independiente de API/Backend ni de una base de datos externa. La aplicación se despliega como una única unidad, de acuerdo con la decisión de utilizar un monolito modular.

La relación entre la vista C4 y el código debe mantenerse alineada con esta implementación:

```text
Aplicación EnAgenda
│
├── Entrada web
│   └── Flask + Jinja2
│
└── Módulo de Invitaciones
    ├── Aplicación
    │   └── GestionarInvitacion
    │
    ├── Dominio
    │   ├── Invitacion
    │   └── EstadoInvitacion
    │
    └── Infraestructura
        └── RepositorioInvitacionesMemoria
```

Si en una evolución posterior se incorpora una base de datos permanente u otros componentes desplegables independientes, los diagramas C4 y esta vista deberán actualizarse para reflejar la nueva arquitectura.