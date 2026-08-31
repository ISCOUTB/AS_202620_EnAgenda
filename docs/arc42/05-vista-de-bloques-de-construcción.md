# 5. Vista de Bloques de Construcción



## 5.1 Descomposición del sistema

EnAgenda se organiza en diferentes módulos funcionales dentro de
`docs/src`. Actualmente se encuentran definidos los siguientes bloques:

- Eventos
- Invitaciones
- agenda
- compartido
- panel
- presupuesto
- tareas

Estos bloques representan las áreas funcionales previstas para el sistema.
El nivel de implementación puede variar entre los diferentes módulos.

A nivel de arquitectura, el sistema contempla una aplicación web, un
portal para invitados, un backend encargado de procesar las solicitudes
y una base de datos, de acuerdo con el C4 nivel 2.

## 5.2 Bloque de Invitaciones

El bloque de Invitaciones es el módulo que actualmente cuenta con una
implementación identificable en el código. Se encuentra en:

`docs/src/Invitaciones/`

Está organizado en tres partes principales:

- `aplicacion`
- `dominio`
- `infraestructura`

### Aplicación

Ruta:

`docs/src/Invitaciones/aplicacion/gestionar_invitacion.py`

Su responsabilidad es coordinar las operaciones relacionadas con la
gestión de invitaciones. Esta capa utiliza las entidades del dominio y
el repositorio para realizar las operaciones correspondientes.

### Dominio

Ruta:

`docs/src/Invitaciones/dominio/invitacion.py`

Contiene la entidad `Invitacion` y el enumerado `EstadoInvitacion`.

La entidad representa una invitación y contiene:

- token de identificación;
- destinatario;
- fecha límite de respuesta;
- estado de la invitación.

También contiene las reglas relacionadas con la creación de una
invitación, la comprobación de su vigencia y el cambio de estado.

Los estados definidos son:

- `PENDIENTE`
- `CONFIRMADO`
- `NO_ASISTIRE`

### Infraestructura

Ruta:

`docs/src/Invitaciones/infraestructura/repositorio_memoria.py`

Contiene `RepositorioInvitacionesMemoria`, encargado de almacenar las
invitaciones en memoria y recuperarlas mediante su token.

## 5.3 Relación entre los bloques

Dentro del módulo de Invitaciones, la aplicación coordina las operaciones
utilizando el dominio y el mecanismo de persistencia proporcionado por
infraestructura.

El flujo principal puede representarse de la siguiente manera:

Aplicación → Dominio

Aplicación → Infraestructura

La aplicación solicita las operaciones necesarias, el dominio aplica las
reglas de la entidad `Invitacion` y la infraestructura permite guardar y
buscar las invitaciones.

## 5.4 Correspondencia entre arquitectura y código

La correspondencia identificada entre los bloques y el código es:

| Bloque | Responsabilidad | Código |
|---|---|---|
| Invitaciones - Aplicación | Coordinar la gestión de invitaciones | `docs/src/Invitaciones/aplicacion/gestionar_invitacion.py` |
| Invitaciones - Dominio | Representar la invitación y sus reglas | `docs/src/Invitaciones/dominio/invitacion.py` |
| Invitaciones - Infraestructura | Guardar y buscar invitaciones en memoria | `docs/src/Invitaciones/infraestructura/repositorio_memoria.py` |

Los demás módulos identificados en `docs/src` forman parte de la
estructura del proyecto, pero no se les atribuyen responsabilidades
específicas en esta sección cuando estas no están respaldadas por una
implementación comprobada.

## 5.5 Relación con C4

La vista de bloques complementa el C4 nivel 2. El C4 identifica los
contenedores principales del sistema: Aplicación Web, Portal del
Invitado, API/Backend y Base de Datos.

La estructura interna mostrada en esta sección permite relacionar el
backend con los módulos que implementan las funcionalidades del sistema.
En el estado actual del proyecto, el módulo de Invitaciones es el bloque
que cuenta con una implementación interna comprobable mediante sus capas
de aplicación, dominio e infraestructura.
