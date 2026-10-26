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

## 8.4 Consistencia de las operaciones implementadas (S12)

PostgreSQL es el almacén durable de usuarios, eventos e invitaciones del flujo
`/eventos`. Las sesiones SQLAlchemy delimitan las transacciones; `flush()` no
confirma, y cerrar una sesión sin `commit()` revierte las escrituras pendientes.
Se usa el aislamiento predeterminado de PostgreSQL (READ COMMITTED, salvo que
el servidor sea configurado de otra forma). No se afirma serialización global.

| Operación real | Garantía y mecanismo | Límite / verificación |
|---|---|---|
| Crear evento (`crear_evento.py`) | Bloquea la fila del usuario con `FOR UPDATE`, cuenta activos, inserta y confirma. Hasta cuatro eventos activos por usuario si las altas pasan por este servicio. | No es un límite mensual. Escrituras SQL externas pueden omitir la regla. La concurrencia requiere prueba en PostgreSQL. |
| Agregar invitados (`agregar_invitados.py`) | Valida el lote completo; bloquea el evento antes de contar y comprobar correos; todos los `flush()` comparten un único `commit()`. Máximo 30 y sin correos repetidos entre altas que usan este servicio. | `test_consistencia_s12.py` comprueba lote inválido, reversión tras un primer flush, límite, duplicado y propietario. SQLite prueba atomicidad, no `FOR UPDATE`. No hay restricción UNIQUE(evento_id, correo) en el esquema actual. |
| Responder invitación de evento (`ver_invitacion_evento`, `app/web.py`) | Bloquea el evento y relee la invitación; comprueba plazo y estado antes de confirmar. Repetir el mismo estado conserva el resultado; entre respuestas distintas válidas queda la última confirmada. | No hay historial de respuestas ni clave de idempotencia. Los escritores futuros del estado del evento deben bloquear esa misma fila. |
| Consultar invitados (`invitados_evento`) | Lee PostgreSQL en cada petición; una petición posterior a un commit ve los cambios confirmados. | La pantalla abierta necesita recargar; no hay WebSocket ni actualización automática. |
| Crear y responder por rutas heredadas (`/crear-invitaciones`, `/invitacion`, `/api/v1/invitaciones`) | Almacén en memoria por proceso. El lote se valida antes de su primera escritura para evitar altas parciales por campos faltantes. | No tiene durabilidad ni coordinación entre workers. No comparte tokens con `/eventos/invitacion`. No es una transacción PostgreSQL ni garantiza reversión ante un fallo inesperado a mitad de escritura. |

### Contraste de dos operaciones con el código

1. **Alta de invitados:** la consulta con `with_for_update()` se realiza sobre
   el evento antes de `contar_por_evento`; `guardar()` solo hace `flush()`;
   `sesion.commit()` aparece después del bucle. Una excepción en la segunda
   inserción cierra la sesión y revierte también la primera. La prueba
   `test_error_despues_del_primer_flush_revierte_todo` inyecta ese fallo y
   comprueba cero filas desde una nueva sesión.
2. **Respuesta de invitación:** `ver_invitacion_evento` obtiene el bloqueo del
   evento, ejecuta `refresh(invitacion)`, comprueba la fecha límite y solo
   confirma si el estado solicitado es válido. GET no modifica asistencia.
   No responder mantiene `pendiente`: debe interpretarse como no confirmado,
   sin afirmar que se cambia automáticamente a `no_asistire`.

## 8.5 Caché e invalidación

**Decisión actual: no introducir una caché de negocio.** Qué: no se cachean
invitaciones, estados ni conteos. Dónde: se consultan directamente en PostgreSQL.
Cuánto: no hay TTL ni retención de resultados entre solicitudes. El límite de
cuatro eventos activos y 30 invitados por evento favorece consultas simples;
no hay medición que justifique Redis ni el riesgo de mostrar una respuesta vieja.
La identidad de objetos de SQLAlchemy solo vive dentro de la sesión de trabajo;
no constituye una caché compartida entre peticiones.

**Invalidación tras escritura: no aplica a una caché externa inexistente.** Tras
el commit del alta se redirige a una petición que consulta de nuevo. Tras responder,
la página muestra el estado confirmado y las posteriores consultas leen la base.
Las páginas con enlaces individuales se entregan con `Cache-Control: no-store`
para evitar retención HTTP de información privada. El almacén heredado en memoria
es una fuente primaria temporal, nunca una caché de PostgreSQL.

Si se introduce caché en el futuro, deberá tener ADR, claves por evento y token,
TTL medido e invalidación después de commit al agregar o responder; no se atribuye
esa propuesta a la implementación actual.

## 8.6 Integración y fallos

El flujo es síncrono HTTP/SQL, sin broker ni publicación de eventos. Entrega,
orden, reintentos de mensajes y cola de errores no aplican. Ante timeout el cliente
no puede inferir si hubo commit: debe consultar el estado antes de repetir.
Repetir una respuesta con el mismo estado es idempotente respecto al estado final;
repetir un alta de invitados devuelve error por correo ya registrado. Crear eventos
no tiene clave de idempotencia: un reintento puede crear otro evento mientras haya
cupo. No se promete entrega exactamente una vez.
