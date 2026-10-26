# 0004 — Evaluar el envío asíncrono de invitaciones mediante un proveedor simulado

- Estado: aceptado.
- Fecha: 2026-10-25.
- Decide: equipo EnAgenda.
- Operación evaluada: envío automático de enlaces individuales de invitación.
- Alcance: prototipo aislado para el taller de mensajes y consistencia.

## Contexto

EnAgenda debe permitir que los enlaces individuales de invitación se envíen
automáticamente desde la aplicación.

Esta operación depende de un proveedor externo de comunicación, que puede
presentar demoras, indisponibilidad temporal o respuestas ambiguas. Por ello,
es necesario evaluar cómo manejar los reintentos y evitar envíos duplicados.

El taller utiliza un proveedor simulado para verificar estas propiedades sin
enviar correos reales, utilizar credenciales ni modificar el despliegue actual.

El canal `correo_simulado` es una elección del experimento y no representa
la selección definitiva de un proveedor para EnAgenda.

## Alternativas consideradas

### A. Envío síncrono

El caso de uso de Invitaciones solicita el envío al proveedor externo durante
la misma solicitud HTTP iniciada por el propietario.

A favor:

- Requiere menos componentes.
- Permite comunicar inmediatamente si el proveedor aceptó o rechazó el envío.
- Reduce la complejidad inicial de implementación y operación.

En contra:

- El tiempo de respuesta de la aplicación depende del proveedor.
- Una falla temporal puede interrumpir la operación iniciada por el usuario.
- Los reintentos pueden prolongar la solicitud HTTP.
- También requiere controlar duplicados y respuestas ambiguas del proveedor.

### B. Envío asíncrono mediante una cola y un consumidor

La aplicación registra una solicitud de envío y un consumidor la procesa
posteriormente, sin mantener abierta la solicitud HTTP durante el envío.

A favor:

- Desacopla temporalmente la solicitud del propietario y el intento de envío.
- Permite reintentar fallos temporales sin que el usuario repita la operación.
- Permite aplicar backoff y conservar mensajes fallidos para revisión.
- Facilita el seguimiento de cada solicitud mediante identificadores.

En contra:

- Requiere una cola y registros durables para una integración productiva.
- Introduce estados pendientes, aceptados y fallidos.
- Puede producir reentregas que deben manejarse mediante idempotencia.
- Requiere operación, seguimiento y tratamiento de mensajes fallidos.
- Confirmar el encolado no significa que la invitación haya sido enviada
  ni recibida por el destinatario.

## Decisión propuesta

Evaluar el envío asíncrono mediante un prototipo aislado con un proveedor
simulado.

El prototipo representa una operación requerida por EnAgenda: el envío
automático de enlaces individuales de invitación. No representa la
actualización del resumen de asistencia de Panel.

Por ahora no se integra este código al flujo Flask ni al despliegue en
Dokploy. La integración productiva queda pendiente de definir el proveedor
real, la persistencia de trabajos, la seguridad y el tratamiento de fallos
entre la aceptación del proveedor y el registro local del resultado.

Esta decisión no rechaza el envío automático ni la utilidad de la mensajería.
Delimita qué se verifica en el taller y qué falta para una integración real.

## Contrato y compatibilidad

El mensaje utilizado es el comando `EnviarInvitacion`, con versión de
contrato `1`.

Contiene:

- `message_id`: identifica un mensaje inmutable.
- `message_type`: debe ser `EnviarInvitacion`.
- `schema_version`: versión del contrato.
- `data.envio_id`: identifica la solicitud lógica de envío.
- `data.invitacion_id`: identifica la invitación.
- `data.canal`: canal simulado utilizado.
- `data.destinatario`: destinatario ficticio.
- `data.enlace`: enlace ficticio de invitación.

Los campos adicionales opcionales son compatibles con la versión 1.
Eliminar campos obligatorios, cambiar sus tipos o modificar su significado
requiere una nueva versión mayor.

Los contratos inválidos y las versiones no soportadas se envían a fallidos
sin reintentos.

## Garantía de entrega y manejo de duplicados

El prototipo simula entrega al menos una vez durante la ejecución del proceso.

Los reintentos conservan el mismo `message_id` y `envio_id`. La deduplicación
se realiza mediante los mensajes procesados y las solicitudes de envío
aceptadas.

El proveedor simulado también utiliza `envio_id` como clave idempotente.
Un reenvío intencional nuevo requiere un nuevo `envio_id`.

No se permite reutilizar una clave de envío con un destinatario o enlace
diferente.

La aceptación por el proveedor simulado no demuestra entrega ni lectura
por parte del invitado.

## Reintentos y mensajes fallidos

- Máximo: tres intentos totales.
- Después del primer fallo temporal: reintento con demora de 1 segundo.
- Después del segundo fallo temporal: reintento con demora de 2 segundos.
- Después del tercer fallo temporal: traslado a mensajes fallidos.
- Los mensajes fallidos conservan el contenido original, los intentos y
  el motivo del fallo.

Las demoras se verifican mediante un reloj virtual, sin esperas reales.

## Observabilidad y verificación

Los logs JSONL permiten seguir una solicitud desde el productor hasta el
consumidor y el proveedor simulado mediante `message_id` y `envio_id`.

Se registran las etapas de producción, entrega, intento de envío, reintento,
aceptación, duplicado ignorado y traslado a fallidos.

Las pruebas automatizadas incluyen:

- Envío aceptado.
- Mensaje duplicado.
- Misma solicitud de envío con otro identificador de mensaje.
- Fallo temporal recuperable.
- Backoff y agotamiento de intentos.
- Compatibilidad con campos opcionales.
- Rechazo de versiones no soportadas.
- Rechazo de contratos incompletos.
- Trazabilidad sin registrar destinatarios ni enlaces.

Los resultados de ejecución deben consultarse en la evidencia del taller.
No se considera verificado un run de GitHub Actions hasta revisar su resultado.

## Consecuencias y límites

Positivas:

- Permite evaluar una operación real del alcance de EnAgenda.
- Demuestra duplicados, reintentos, backoff y mensajes fallidos sin
  contratar servicios.
- No requiere credenciales ni envíos reales.
- Mantiene el experimento separado del MVP.

Limitaciones:

- La cola, la deduplicación y los resultados se conservan en memoria.
- No existe durabilidad frente a reinicios.
- No se demuestra atomicidad entre PostgreSQL y la publicación del mensaje.
- No se evalúa concurrencia ni carga.
- No se demuestra recuperación ante una caída después de la aceptación
  remota y antes del registro local.
- No se garantiza entrega exactamente una vez.
- No se implementa el reproceso operativo de mensajes fallidos.
- No se selecciona ni configura un proveedor real de envío.

## Criterios para integrar posteriormente

Antes de incorporar el mecanismo al sistema se debe:

1. Seleccionar el proveedor y el canal real.
2. Definir almacenamiento durable para trabajos y resultados.
3. Resolver la coordinación entre guardar la invitación y registrar
   su solicitud de envío.
4. Definir idempotencia o reconciliación ante respuestas ambiguas.
5. Proteger credenciales, destinatarios y enlaces.
6. Probar el flujo integrado y documentar sus costos y límites.

## Trazabilidad

- [Contrato, ejecución y límites](../talleres/mensajes-consistencia/README.md).
- [Simulador](../../experimentos/mensajes_consistencia/simulador.py).
- [Demostración](../../experimentos/mensajes_consistencia/demo.py).
- [Pruebas](../../experimentos/mensajes_consistencia/test_simulador.py).
- [Logs de demostración](../talleres/mensajes-consistencia/resultados/demo.jsonl).
- [Evidencia de pruebas](../talleres/mensajes-consistencia/resultados/pruebas.txt).
- [Workflow](../../.github/workflows/taller-mensajes.yml).