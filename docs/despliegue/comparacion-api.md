# Comparación de alternativas de despliegue — API Flask de EnAgenda

## Condición operativa

No fue publicada una condición operativa ni un reto técnico adicional para el
equipo. Esta comparación se realiza con las restricciones vigentes del proyecto:

- Herramientas gratuitas o con capa gratuita.
- No exigir tarjeta ni cuentas personales de pago.
- URL pública accesible fuera de la red de la universidad.
- Repositorio público sin secretos ni datos personales reales.
- Aplicación Flask con persistencia actual en memoria.

## Pieza evaluada

La pieza evaluada es la API Flask de EnAgenda, ubicada principalmente en
`app/web.py`. Expone rutas web, rutas de invitaciones, el health check
`GET /health` y la métrica `GET /metrics`.

No se evalúa el sistema completo ni una base de datos, porque la persistencia
actual se realiza mediante un repositorio en memoria.

## Alternativas evaluadas

1. Render Free Web Service.
2. Servidor del laboratorio.

## Supuestos

- La API se ejecuta con Python 3.13, Flask y Gunicorn.
- Se estima un tráfico bajo y esporádico de [COMPLETAR] solicitudes mensuales.
- El tamaño medio de una respuesta es de [COMPLETAR] KB.
- El tráfico de salida mensual esperado es de [COMPLETAR] MB.
- La aplicación mantiene una única instancia.
- La persistencia no es durable; los datos se pierden si el proceso se reinicia.
- El escenario de calidad de latencia de la API es [COMPLETAR O ENLAZAR].
- La aplicación debe poder consultarse desde fuera de la red universitaria.

## Comparación

| Criterio | Render Free Web Service | Servidor del laboratorio |
|---|---|---|
| Pieza desplegada | API Flask dentro de un contenedor Docker | API Flask en el mismo contenedor Docker |
| Tarjeta personal | No requerida, verificado el [FECHA] | No requerida |
| URL pública | URL HTTPS proporcionada por Render | Depende de acceso, puerto y URL otorgados por el laboratorio |
| Infraestructura como código | `Dockerfile` y `render.yaml` | `Dockerfile` y `docker-compose.yml` |
| Costo directo | $0 dentro de la capa gratuita | $0 para el equipo, sujeto a recursos otorgados |
| Tráfico esperado | Adecuado para tráfico bajo y esporádico | Depende de recursos disponibles |
| Inactividad | Se suspende tras 15 minutos sin tráfico | Puede mantenerse activo si el laboratorio lo permite |
| Latencia posterior a inactividad | Se mide en `medicion-render.md` | Depende del proceso y la infraestructura del laboratorio |
| Logs | Logs del proveedor + JSON a salida estándar | Logs del contenedor o proceso |
| Métricas | Endpoint `/metrics` | Endpoint `/metrics` |
| Persistencia | No resuelta en esta iteración | No resuelta en esta iteración |
| Reversión | Desplegar la misma imagen en laboratorio | Crear servicio Render usando `render.yaml` |
| Riesgos | Suspensión, cuota compartida y cambios en el plan | Acceso, puertos, disponibilidad y recursos por confirmar |

## Decisión

Se selecciona Render Free Web Service como plataforma temporal para el MVP y la
evidencia de esta semana. Permite una URL pública, despliegue desde GitHub y un
costo monetario estimado de $0.

Se acepta la suspensión posterior a 15 minutos de inactividad como una
limitación conocida. La reactivación se mide y se documenta. El servidor del
laboratorio permanece como alternativa de reversión.

## Evidencia

- URL pública: [COMPLETAR DESPUÉS DEL DESPLIEGUE].
- Health check: [COMPLETAR].
- Métricas: [COMPLETAR].
- Pipeline: [COMPLETAR].
- Medición de Render: [medicion-render.md](medicion-render.md).
- Costos: [costos.md](costos.md).
- Procedimiento: [procedimiento-despliegue.md](procedimiento-despliegue.md).
- ADR: [ADR-0003](../adr/0003-desplegar-api-flask-en-render.md).