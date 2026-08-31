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

Actualmente se encuentra implementado un corte vertical mínimo del módulo de **Invitaciones**.

Este flujo permite:

1. Crear una invitación.
2. Generar un token individual.
3. Consultar una invitación mediante su token.
4. Mostrar la invitación mediante una interfaz web.
5. Responder si el invitado confirma su asistencia o no asistirá.
6. Persistir la respuesta utilizando un repositorio en memoria.

El flujo actual atraviesa la interfaz, la lógica de aplicación, el dominio y la infraestructura:

```text
Interfaz web
    ↓
GestionarInvitacion
    ↓
Invitacion
    ↓
RepositorioInvitacionesMemoria
```

## Requisitos

Para ejecutar el proyecto se necesita:

* Python 3.13 o compatible.
* pip.

## Instalación

Después de clonar el repositorio, instalar las dependencias con:

```bash
python -m pip install -r requerimiento.txt
```

Las dependencias principales son:

* Flask 3.1.3
* pytest 8.x

## Ejecutar las pruebas

Desde la raíz del proyecto ejecutar:

```bash
pytest -q
```

Las pruebas actuales deben finalizar correctamente.

## Ejecutar la aplicación

Desde la raíz del proyecto ejecutar:

```bash
python app\web.py
```

Cuando Flask indique que está ejecutándose, abrir en el navegador:

```text
http://127.0.0.1:5000
```

La interfaz permite consultar una invitación de prueba y responder:

* Confirmar asistencia.
* No asistiré.

## Estructura actual del proyecto

```text
AS_202620_EnAgenda/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── __init__.py
│   └── web.py
├── src/
│   └── invitaciones/
│       ├── aplicacion/
│       ├── dominio/
│       └── infraestructura/
├── tests/
│   └── test_invitaciones.py
├── docs/
│   ├── adr/
│   ├── arc42/
│   ├── arquitectura/
│   └── c4/
├── .gitignore
├── README.md
└── requerimiento.txt
```

## Integración continua

El proyecto cuenta con un flujo de integración continua en:

```text
.github/workflows/ci.yml
```

El flujo instala Python, instala las dependencias definidas en `requerimiento.txt` y ejecuta las pruebas automáticamente en GitHub Actions.

De esta forma se puede verificar que los cambios realizados mantengan las pruebas funcionando correctamente.
