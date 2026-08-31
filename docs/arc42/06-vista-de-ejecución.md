# 6. Vista de Ejecución

## 6.1 Escenario: responder una invitación

Un escenario de ejecución implementado actualmente en EnAgenda es la
respuesta a una invitación.

El usuario proporciona el token de la invitación, el nuevo estado de
respuesta y la fecha y hora actual. La operación es coordinada por la
clase `GestionarInvitacion`.

El recorrido atraviesa las capas de aplicación, dominio e
infraestructura.

## 6.2 Flujo de ejecución

El flujo principal es el siguiente:

1. La operación llega a `GestionarInvitacion.responder()` con el token,
   el estado seleccionado y la fecha y hora actual.

2. La capa de aplicación consulta la invitación mediante
   `RepositorioInvitacionesMemoria.buscar_por_token()`.

3. Si la invitación no existe, se genera un error indicando que la
   invitación no fue encontrada.

4. Si la invitación existe, se comprueba mediante
   `Invitacion.esta_vigente()` que todavía se encuentre dentro de la
   fecha límite.

5. La entidad `Invitacion` ejecuta `cambiar_estado()` para validar y
   actualizar el estado de la invitación.

6. La capa de aplicación guarda nuevamente la invitación utilizando
   `RepositorioInvitacionesMemoria.guardar()`.

7. Finalmente, la invitación actualizada es retornada como resultado de
   la operación.

## 6.3 Interacción entre bloques

El recorrido puede representarse de la siguiente manera:

Usuario
  ↓
GestionarInvitacion
  ↓
RepositorioInvitacionesMemoria
  ↓
Invitacion
  ↓
RepositorioInvitacionesMemoria
  ↓
Invitacion actualizada

La clase `GestionarInvitacion` coordina el caso de uso. El repositorio
permite recuperar y almacenar la invitación, mientras que la entidad
`Invitacion` aplica las reglas relacionadas con su vigencia y estado.

## 6.4 Correspondencia con el código

El escenario se encuentra implementado en las siguientes rutas:

- Aplicación:
  `docs/src/Invitaciones/aplicacion/gestionar_invitacion.py`

- Dominio:
  `docs/src/Invitaciones/dominio/invitacion.py`

- Infraestructura:
  `docs/src/Invitaciones/infraestructura/repositorio_memoria.py`

El método principal del escenario es
`GestionarInvitacion.responder()`, que consulta la invitación, solicita
el cambio de estado a la entidad y posteriormente guarda el resultado.

## 6.5 Manejo de situaciones no válidas

Durante la ejecución se contemplan situaciones en las que la operación
no puede continuar:

- Si el token no corresponde a una invitación existente, se genera el
  error "Invitación no encontrada".
- Si la invitación ya superó su fecha límite, se genera el error
  correspondiente a una invitación vencida.
- Si el nuevo estado no pertenece a `EstadoInvitacion`, el dominio
  rechaza el cambio de estado.

De esta manera, las reglas del dominio se mantienen dentro de la entidad
`Invitacion`, mientras que la capa de aplicación coordina el flujo de
ejecución.
