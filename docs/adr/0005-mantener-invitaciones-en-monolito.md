# 0005 — Mantener Invitaciones dentro del monolito

- Estado: Aceptado.
- Fecha: 2026-11-23.
- Alcance: decisión de extracción del módulo Invitaciones.
- No reemplaza la decisión del taller de mensajería.

## Contexto

EnAgenda utiliza Flask y PostgreSQL para el flujo persistente de eventos e
invitaciones. También conserva rutas heredadas con almacenamiento en memoria.
El taller evalúa envíos mediante un proveedor simulado aislado, no integrado
a la aplicación.

Debemos decidir si extraer Invitaciones a un servicio independiente mejora
suficientemente la solución actual para justificar su costo.

## Alternativas

| Alternativa | Beneficios | Costos y riesgos |
|---|---|---|
| Mantener Invitaciones como módulo interno | Conserva llamadas internas y transacciones locales; evita otro despliegue y permite concentrarse en verificar el flujo actual. | Comparte proceso y disponibilidad con Flask; exige disciplina para mantener límites entre módulos. |
| Extraer Invitaciones como servicio independiente | Permitiría despliegue y escalado separados; podría aislar ciertos fallos internos si se diseña adecuadamente. | Introduce comunicación de red, autenticación entre servicios, contratos remotos, timeouts, observabilidad distribuida y revisión de propiedad de datos. No garantiza por sí sola mayor disponibilidad. |
| Extraer únicamente el envío a un consumidor | Podría separar esperas del proveedor y reintentos de la solicitud web. | Requiere proveedor definido, trabajos durables, deduplicación y coordinación entre guardar la invitación y registrar el envío. El simulador no resuelve todavía esa integración. |

## Decisión propuesta

Mantener Invitaciones dentro del monolito y no incorporar el simulador al
flujo productivo en esta versión.

No existe evidencia medida que justifique asumir ahora el costo de una
extracción. La prioridad es verificar persistencia, seguridad, consistencia,
despliegue y recuperación del sistema existente.

Esta decisión no descarta la necesidad futura de envío automático.

## Consecuencias

- No se introduce un nuevo servicio, broker ni protocolo remoto.
- Se conserva el riesgo de indisponibilidad conjunta del monolito.
- La caída de PostgreSQL sigue afectando las operaciones persistentes.
- Deben respetarse los límites del módulo y corregirse los caminos heredados.
- La mensajería del taller conserva valor experimental, sin presentarse como
  funcionalidad integrada.

## Condiciones para revisar la decisión

Reevaluar si se demuestra alguna de estas condiciones:

- Carga medida que requiera escalado independiente.
- Necesidad operativa de despliegues separados.
- Fallos de un proveedor real que deban aislarse.
- Equipo y recursos suficientes para operar otro servicio.
- Estrategia durable y probada para trabajos, reintentos y duplicados.

## Verificación y límites

La ejecución conjunta registra 35 pruebas aprobadas. No constituye una
comparación experimental de monolito frente a microservicios ni una prueba
de disponibilidad pública.

Los modos de fallo incluyen controles existentes y pendientes declarados.
No se atribuye implementación a las mitigaciones todavía propuestas.

## Trazabilidad

- [Fallos y deuda técnica](../arc42/11-riesgos-y-deuda-técnica.md).
- [Consistencia y caché](../arc42/08-conceptos-transversales.md).
- [Aplicación Flask](../../app/web.py).
- [Módulo Invitaciones](../../src/invitaciones/).
- [Pruebas integradas](../evidencias/pruebas-integradas.txt).
- [Taller aislado](../talleres/mensajes-consistencia/README.md).