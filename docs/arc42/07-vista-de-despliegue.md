# 7. Vista de despliegue

## 7.1 Nivel 1: infraestructura

```text
Usuario externo
      │ HTTPS
      ▼
Render Free Web Service
┌──────────────────────────────────────────────┐
│ Contenedor Docker                            │
│ - Python 3.13                                │
│ - Gunicorn                                   │
│ - Aplicación Flask                           │
│ - Módulo Invitaciones                        │
│ - GET /health                                │
│ - GET /metrics                               │
│ - Logs JSON hacia salida estándar            │
└──────────────────────────────────────────────┘
      │
      ▼
Repositorio en memoria
(no persistente; se pierde durante reinicio)
```

## 7.2 Piezas y ubicación

| Pieza | Ubicación | Tecnología | Estado |
|---|---|---|---|
| API web | Render Free Web Service | Docker, Python, Flask y Gunicorn | Implementada |
| Módulo de Invitaciones | Dentro del contenedor de la API | Python | Implementada |
| Persistencia | Memoria del proceso | Repositorio en memoria | Temporal; no durable |
| Integración continua | GitHub Actions | Workflow YAML | Implementada |
| Logs | Panel de logs de Render | JSON por salida estándar | Implementada |
| Métricas | Endpoint `/metrics` | JSON en memoria | Implementada |
| Secretos | Variables de entorno de Render | `SECRET_KEY` | Implementada |
| Base de datos | No implementada | — | Deuda técnica |

## 7.3 Restricciones y riesgos

Render Free puede suspender el servicio tras 15 minutos de inactividad. La
primera solicitud posterior puede tardar mientras el servicio se reactiva. La
limitación es aceptada para el MVP y se mide en
[medicion-render.md](../despliegue/medicion-render.md).

La persistencia en memoria pierde invitaciones durante reinicios, redeploys o
caídas del proceso. Esta limitación no es adecuada para una versión productiva
y se registra como deuda técnica.

## 7.4 Reversión

La aplicación se empaqueta en un contenedor Docker independiente del proveedor.
La reversión consiste en desplegar el mismo commit e imagen en el servidor del
laboratorio, siguiendo el
[procedimiento documentado](../despliegue/procedimiento-despliegue.md).