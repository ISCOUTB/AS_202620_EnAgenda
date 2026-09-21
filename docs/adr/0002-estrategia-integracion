# 0002 — Estrategia de integración síncrona para la API

- Estado: Aceptado
- Fecha: 2026-09-21
- Decide: Equipo EnAgenda
- Escenarios de calidad relacionados: EC-01, EC-02, EC-03 y EC-04

## Contexto

EnAgenda necesita definir una estrategia de integración para las operaciones expuestas mediante su interfaz HTTP.

Las operaciones relacionadas con las invitaciones requieren una respuesta inmediata para que el usuario pueda conocer el resultado de una acción, por ejemplo consultar una invitación o registrar una respuesta de asistencia.

El sistema debe mantener la consistencia de la información y validar reglas de negocio como la vigencia de una invitación y los estados permitidos.

Además, el contrato de la API debe estar definido de forma ejecutable y versionada mediante OpenAPI, de manera que la estructura de las solicitudes y respuestas pueda ser comprobada automáticamente.

La arquitectura general de EnAgenda continúa utilizando un monolito modular. Por lo tanto, la estrategia de integración debe mantener una solución sencilla y adecuada para el alcance actual del proyecto, sin introducir infraestructura de mensajería innecesaria.

## Alternativas consideradas

### A. Integración síncrona mediante HTTP y JSON

La integración síncrona permite que el cliente realice una solicitud HTTP y espere la respuesta del servidor antes de continuar con la operación.

#### A favor

- Permite obtener una respuesta inmediata después de cada operación.
- Es adecuada para operaciones como consultar una invitación o registrar una respuesta.
- Facilita la validación de solicitudes y respuestas mediante un contrato OpenAPI.
- Es sencilla de probar y depurar.
- No requiere incorporar infraestructura adicional de mensajería.
- Se ajusta al alcance actual de EnAgenda y al uso de una aplicación web como cliente.

#### En contra

- El cliente debe esperar la respuesta del servidor.
- Una indisponibilidad temporal del servidor puede impedir completar la operación.
- Las operaciones de larga duración no serían adecuadas para este mecanismo.

#### Por qué se eligió

La mayoría de las operaciones actuales de EnAgenda requieren conocer inmediatamente si la acción fue aceptada o rechazada.

Por ejemplo, cuando un invitado responde una invitación, el sistema debe validar que el enlace siga vigente, comprobar que el nuevo estado sea válido y comunicar el resultado de la operación.

Por estas razones, la comunicación síncrona mediante HTTP y JSON resulta adecuada para las necesidades actuales del sistema.

### B. Integración asíncrona mediante mensajería

La integración asíncrona utiliza mensajes o eventos para que el emisor pueda continuar sin esperar una respuesta inmediata del receptor.

#### A favor

- Reduce el acoplamiento temporal entre los participantes.
- Puede ser útil para procesos que no necesitan una respuesta inmediata.
- Permite procesar determinadas tareas de forma diferida.

#### En contra

- Requiere incorporar mecanismos adicionales de mensajería.
- Aumenta la complejidad de desarrollo, pruebas y operación.
- Introduce aspectos adicionales como colas, reintentos, procesamiento duplicado y manejo de mensajes.
- No aporta un beneficio directo para las operaciones interactivas actuales de EnAgenda.

#### Por qué no se eligió

Para el alcance actual del proyecto no existe una necesidad que justifique incorporar mensajería asíncrona.

Las operaciones principales requieren una respuesta inmediata para informar al usuario sobre el resultado de su acción. Introducir una infraestructura de eventos o colas aumentaría la complejidad sin resolver una necesidad actual.

## Decisión

Se utilizará una estrategia de integración síncrona mediante HTTP y JSON para las operaciones de la API de EnAgenda.

El contrato de la API se documentará mediante OpenAPI y se mantendrá versionado junto con el código fuente.

Las solicitudes serán procesadas de forma síncrona y las respuestas utilizarán el formato JSON cuando corresponda.

La comunicación seguirá el siguiente esquema general:

```text
Cliente
   |
   | HTTP/JSON
   v
API de EnAgenda
   |
   | ejecución síncrona
   v
Módulos de aplicación y dominio
   |
   v
Respuesta HTTP/JSON
   |
   v
Cliente
