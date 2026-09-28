# 0003 — Desplegar la API Flask en Render Free

- **Estado:** aceptado
- **Fecha:** 2026-09-27
- **Decide:** [COMPLETAR CON INTEGRANTES]
- **Escenario de calidad relacionado:** EC-03 — Observabilidad de solicitudes
- **Aspecto relacionado:** A-01 — Gestión de invitaciones

## Contexto

EnAgenda requiere una URL pública accesible fuera de la red de la universidad.
La pieza evaluada es la API Flask, que expone rutas web, rutas de invitaciones,
el health check `GET /health` y la métrica `GET /metrics`.

El proyecto está sujeto a una restricción de costo: se deben usar herramientas
gratuitas o capas gratuitas sin exigir tarjeta personal. La persistencia actual
se realiza en memoria y los datos se pierden después de un reinicio o redeploy.

## Alternativas consideradas

### A. Render Free Web Service

**A favor:**

- Proporciona una URL HTTPS pública.
- Puede desplegar automáticamente desde el repositorio.
- Permite versionar la configuración mediante `render.yaml`.
- Puede ejecutar la API Flask dentro de un contenedor Docker.
- Tiene costo monetario estimado de $0 dentro de la capa gratuita.

**En contra:**

- Suspende el servicio después de 15 minutos de inactividad.
- La primera solicitud posterior puede tardar mientras se reactiva.
- Las horas gratuitas son compartidas por workspace.
- No proporciona persistencia durable para el estado actual de la aplicación.

### B. Servidor del laboratorio

**A favor:**

- No exige tarjeta personal.
- Permite ejecutar la misma imagen Docker.
- Puede evitar la suspensión por inactividad si se mantiene el proceso activo.
- Permite revertir el despliegue sin modificar el código de dominio.

**En contra:**

- El acceso, puertos públicos, disponibilidad y recursos están pendientes de
  confirmación.
- El equipo asume mayor responsabilidad operativa.
- No permite un despliegue inmediato mientras no se otorgue acceso.

## Decisión

Se elige Render Free Web Service para desplegar temporalmente la API Flask de
EnAgenda durante el MVP académico. Esta alternativa permite cumplir la
evidencia de URL pública, infraestructura versionada, CI, health check, logs
estructurados y métricas con un costo monetario inicial estimado de $0.

La suspensión después de inactividad se acepta como limitación conocida. Se
mide y se documenta el tiempo de reactivación. El servidor del laboratorio se
mantiene como alternativa de reversión.

## Consecuencias

- **Positivas:** URL pública, integración con GitHub, despliegue reproducible
  con Docker y `render.yaml`, y costo inicial estimado de $0.
- **Negativas:** demora potencial en la primera solicitud tras inactividad,
  cuota compartida de la capa gratuita y pérdida de datos por persistencia en
  memoria.
- **Riesgos:** si el comportamiento posterior a inactividad incumple el
  escenario de calidad, si se superan los límites gratuitos o si se necesita
  persistencia durable, será necesario migrar al servidor del laboratorio o
  reevaluar otra plataforma.
- **Revisión futura:** al añadir una base de datos persistente se debe crear un
  ADR específico sobre persistencia, respaldo y costos.

## Procedimiento de reversión

1. Conservar `Dockerfile`, `docker-compose.yml` y variables de entorno
   independientes de Render.
2. Usar el último commit estable de la rama principal.
3. Desplegar el mismo contenedor en el servidor del laboratorio.
4. Configurar `SECRET_KEY` solo en el entorno del servidor.
5. Verificar `GET /health`, `GET /metrics` y `pytest -q`.
6. Actualizar las URL públicas en README y en la evidencia.

## Trazabilidad

- Aspecto: A-01 — Gestión de invitaciones.
- Implementación: `app/web.py`, `Dockerfile`, `docker-compose.yml`,
  `render.yaml`.
- Pruebas: `tests/test_operacion.py`.
- Evidencia: URL pública, pipeline CI, health check, métricas, logs y
  `docs/despliegue/medicion-render.md`.