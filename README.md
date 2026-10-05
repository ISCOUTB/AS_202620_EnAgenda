# AS_202620_EnAgenda

EnAgenda es una aplicación creada para ayudar a organizar eventos pequeños de una manera más sencilla y ordenada. La idea principal es tener en un solo lugar toda la información relacionada con un evento, en vez de tenerla repartida entre chats, notas, hojas de cálculo o diferentes aplicaciones.

Con EnAgenda se podrá llevar el control de los invitados, las confirmaciones de asistencia, las tareas pendientes, los elementos que hacen falta, la agenda del evento y los gastos. De esta forma, será más fácil saber qué cosas ya están listas y cuáles todavía necesitan atención.

## Problema

Cuando se organiza un evento pequeño, normalmente aparecen muchas cosas que hay que recordar: quiénes van a asistir, qué falta por comprar, qué tareas están pendientes, cuánto se ha gastado y qué actividades se deben realizar durante el evento.

Muchas veces esta información termina repartida entre conversaciones de WhatsApp, notas del celular, hojas de cálculo o simplemente queda en la memoria de la persona que está organizando.

Esto puede hacer que se olviden tareas, se pierdan datos importantes o sea difícil tener una idea clara de cómo va la organización.

Por eso surge EnAgenda, como una herramienta que reúne toda esta información en un mismo lugar y permite llevar un mejor control del evento.

## Usuarios principales

### Propietario del evento

Es la persona que se encarga de organizar el evento. Podrá crear el evento y administrar toda la información relacionada con él, como:

* Información general del evento.
* Lista de invitados.
* Confirmaciones de asistencia.
* Tareas pendientes.
* Elementos que se necesitan.
* Agenda y horarios.
* Presupuesto y gastos.
* Estado de preparación del evento.

### Invitado

Es la persona que recibe una invitación al evento. Podrá ver la información que el organizador haya compartido y responder si asistirá o no.

Para hacerlo más sencillo, el invitado no tendrá que crear una cuenta ni descargar la aplicación. Podrá acceder directamente mediante un enlace individual recibido en su invitación.

## Funcionalidades previstas

EnAgenda contará inicialmente con las siguientes funcionalidades:

* Crear, editar, publicar y cancelar eventos.
* Agregar y administrar invitados.
* Generar un enlace individual para cada invitado.
* Registrar y consultar las confirmaciones de asistencia.
* Crear tareas y marcar su estado.
* Registrar los elementos necesarios para el evento, como comida, decoración o materiales.
* Organizar las actividades del evento mediante una agenda.
* Registrar los gastos estimados y los gastos realizados.
* Mostrar información básica sobre el avance de la organización.

## Estado actual

Actualmente se encuentra implementado un corte vertical funcional del módulo de **Invitaciones**.

Este flujo permite:

1. Seleccionar la cantidad de invitados que tendrá el evento.
2. Definir una fecha y hora límite para responder las invitaciones.
3. Registrar el nombre y correo electrónico de cada invitado.
4. Crear múltiples invitaciones a partir de los datos registrados.
5. Generar un token único para cada invitación.
6. Generar un enlace individual para cada invitado.
7. Consultar una invitación mediante su token.
8. Mostrar cada invitación mediante una interfaz web.
9. Permitir que el invitado confirme su asistencia o indique que no asistirá.
10. Persistir temporalmente las invitaciones y sus respuestas mediante un repositorio en memoria.

La aplicación cuenta actualmente con una interfaz web desarrollada con **Flask, Jinja2, HTML y CSS**, mientras que la lógica del módulo de invitaciones mantiene la separación entre aplicación, dominio e infraestructura.

El flujo actual atraviesa las siguientes capas:

```text
Interfaz web (HTML/CSS + Jinja2)
        ↓
Flask (app/web.py)
        ↓
GestionarInvitacion
        ↓
Invitacion / EstadoInvitacion
        ↓
RepositorioInvitacionesMemoria
```

## Estructura actual del proyecto

```text
AS_202620_EnAgenda/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── static/
│   │   └── css/
│   │       ├── inicio.css
│   │       ├── invitados.css
│   │       ├── invitacion.css
│   │       ├── invitacion_creada.css
│   │       └── invitaciones_creadas.css
│   │
│   ├── templates/
│   │   ├── inicio.html
│   │   ├── invitados.html
│   │   ├── invitacion.html
│   │   ├── invitacion_creada.html
│   │   └── invitaciones_creadas.html
│   │
│   ├── __init__.py
│   └── web.py
│
├── src/
│   ├── agenda/
│   ├── compartido/
│   ├── eventos/
│   ├── invitaciones/
│   │   ├── aplicacion/
│   │   ├── dominio/
│   │   └── infraestructura/
│   ├── panel/
│   ├── presupuesto/
│   └── tareas/
│
├── tests/
│   ├── test_api_invitaciones.py
│   ├── test_contrato_openapi.py
│   ├── test_invitaciones.py
│   └── test_operacion.py
│
├── docs/
│   ├── adr/
│   ├── api/
│   ├── arc42/
│   ├── arquitectura/
│   ├── c4/
│   ├── despliegue/
│   ├── aspectos.md
│   ├── correcciones.md
│   ├── evidencia.md
│   ├── ficha-problema.md
│   └── ia.md
│
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requerimiento.txt
```

## Requisitos

Para ejecutar EnAgenda en un entorno local se necesita:

- Python 3.13 o una versión compatible.
- pip para la instalación de dependencias.
- Git para clonar y gestionar el repositorio.

Para el despliegue mediante contenedores se requiere adicionalmente:

- Docker.
- Docker Compose.

## Instalación

Primero, clonar el repositorio:

```bash
git clone https://github.com/ISCOUTB/AS_202620_EnAgenda.git
```

Ingresar a la carpeta del proyecto:

```bash
cd AS_202620_EnAgenda
```

Se recomienda crear un entorno virtual para mantener aisladas las dependencias del proyecto:

```bash
python -m venv .venv
```

En Windows, activar el entorno virtual con:

```bash
.venv\Scripts\activate
```

Instalar las dependencias:

```bash
python -m pip install -r requerimiento.txt
```

Las dependencias principales del proyecto incluyen:

- Flask 3.1.3.
- pytest 8.x.

## Ejecución local

Para iniciar la aplicación:

```bash
python app/web.py
```

Por defecto, la aplicación estará disponible en:

```text
http://127.0.0.1:5000
```

Para detener el servidor se puede utilizar `Ctrl + C`.

## Pruebas

Para ejecutar las pruebas automatizadas del proyecto:

```bash
python -m pytest
```

Las pruebas permiten verificar el comportamiento del módulo de invitaciones, los endpoints de la API y otros aspectos definidos para el proyecto.

## Ejecución con Docker

El proyecto también puede ejecutarse utilizando Docker Compose:

```bash
docker compose up --build
```

Esto construye la imagen de la aplicación y levanta los servicios definidos en `docker-compose.yml`.

Para detener los contenedores:

```bash
docker compose down
```

### Organización de la interfaz web

La interfaz web de EnAgenda se encuentra organizada dentro del directorio `app/`, separando la estructura visual de los estilos.

- `app/templates/`: contiene las plantillas HTML utilizadas por Flask y Jinja2 para representar las diferentes pantallas del flujo de invitaciones.
- `app/static/css/`: contiene las hojas de estilo CSS asociadas a las plantillas de la interfaz.
- `app/web.py`: contiene las rutas HTTP de Flask y conecta la interfaz web con los casos de uso del módulo de invitaciones.

Actualmente, las principales vistas de la interfaz son:

- `inicio.html`: permite definir la cantidad de invitados y la fecha y hora límite de respuesta.
- `invitados.html`: permite registrar el nombre y correo electrónico de cada invitado.
- `invitacion.html`: muestra la invitación al destinatario y permite registrar su respuesta.
- `invitacion_creada.html`: muestra la información de una invitación creada.
- `invitaciones_creadas.html`: presenta las invitaciones generadas y sus respectivos enlaces.

Cada vista cuenta con sus estilos correspondientes dentro de `app/static/css/`.

## Integración continua

El proyecto cuenta con un flujo de integración continua en:

```text
.github/workflows/ci.yml
```

El flujo instala Python, instala las dependencias definidas en `requerimiento.txt` y ejecuta las pruebas automáticamente en GitHub Actions.

De esta forma se puede verificar que los cambios realizados mantengan las pruebas funcionando correctamente.

## Ejecución con Docker

Desde la raíz del repositorio:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

La aplicación queda disponible localmente en:

```text
http://localhost:5000
```

Validaciones locales:

```powershell
curl.exe -i http://localhost:5000/health
curl.exe -i http://localhost:5000/metrics
python -m pytest -q
```

Para detener el entorno:

```powershell
docker compose down
```

El archivo `.env` es local y no debe subirse al repositorio.

## Despliegue institucional

EnAgenda se despliega en Dokploy institucional mediante Docker Compose.

- Repositorio: `ISCOUTB/AS_202620_EnAgenda`.
- Rama de despliegue: `master`.
- Activación: `On Push`.
- Archivo Compose: `./docker-compose.yml`.
- Puerto interno: `5000`.
- Estado del contenedor: desplegado correctamente en Dokploy.
- URL pública: pendiente de crear o asignar un host válido.
- Health check previsto: `http://[host-asignado]/health`.
- Métricas previstas: `http://[host-asignado]/metrics`.

La URL pública y HTTPS se documentarán cuando se configure un dominio o host
válido en Dokploy.
