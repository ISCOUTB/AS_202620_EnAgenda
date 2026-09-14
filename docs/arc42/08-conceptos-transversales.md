# 8. Conceptos transversales

## 8.1 Lenguaje ubicuo

| Término | Significado en EnAgenda |
|---|---|
| Propietario | Usuario que crea y administra un evento. |
| Evento | Unidad principal de organización que contiene fecha, lugar, invitados, tareas, agenda y presupuesto. |
| Invitado | Persona invitada a un evento que puede responder mediante un enlace individual. |
| Invitación | Relación entre un invitado y un evento; contiene un token, vigencia y estado de asistencia. |
| Enlace individual | URL asociada a una invitación específica, usada por el invitado sin crear cuenta. |
| Token | Identificador no predecible incluido en el enlace individual. |
| Fecha límite de respuesta | Fecha y hora a partir de la cual la invitación se cierra, independiente de la fecha del evento. |
| Estado de asistencia | Estado vigente de una invitación: `Pendiente`, `Confirmado` o `No asistiré`. |
| Tarea | Actividad pendiente o completada para preparar un evento. |
| Agenda | Conjunto de actividades programadas con horario durante un evento. |
| Elemento necesario | Recurso requerido para el evento, por ejemplo decoración o mesas. |
| Gasto | Registro de un valor económico asociado al evento. |
| Panel | Vista de seguimiento que resume información de otros contextos sin ser dueño de los datos operativos. |
| Contexto delimitado | Límite funcional dentro del monolito modular que tiene responsabilidades y datos propios. |

## 8.2 Contextos delimitados

EnAgenda se organiza como un monolito modular con los contextos Eventos,
Invitaciones, Tareas, Agenda, Presupuesto y Panel. Cada contexto es responsable
de sus propias reglas y datos.

El mapa de contextos, las relaciones tipificadas y la propiedad de datos se
encuentran en:

[Contextos delimitados y propiedad de datos](../arquitectura/contextos-y-propiedad-de-datos.md)

## 8.3 Regla de propiedad de datos

Cada entidad tiene un único contexto dueño. El contexto dueño concentra las reglas
de negocio y es responsable de validar y persistir cualquier cambio sobre sus
datos.

Los demás contextos pueden consultar la información necesaria mediante servicios,
contratos o resúmenes, pero no deben modificar directamente entidades que
pertenecen a otro contexto.

La propiedad técnica de los datos es diferente de los permisos de los actores del
sistema. El propietario del evento puede administrar la información operativa de
su evento, mientras que el invitado solo puede modificar su propio estado de
asistencia mediante un enlace individual vigente.

Por ejemplo, Invitaciones es el contexto dueño de los tokens y estados de
asistencia. El invitado puede solicitar un cambio entre `Pendiente`,
`Confirmado` y `No asistiré`, pero el módulo Invitaciones valida la vigencia del
enlace y guarda el único estado vigente. El Panel solo consulta conteos o
resúmenes y no crea ni modifica invitaciones.