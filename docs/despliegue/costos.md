# Estimación mensual de costos — API Flask de EnAgenda

## Pieza estimada

API Flask de EnAgenda desplegada como un Render Free Web Service.

## Supuestos

- Solicitudes mensuales: [COMPLETAR].
- Tamaño promedio de respuesta: [COMPLETAR] KB.
- Tráfico de salida estimado: [COMPLETAR] MB.
- Instancias: 1.
- Persistencia: repositorio en memoria; no se contrata base de datos.
- Pipeline: GitHub Actions para repositorio público.
- El servicio permanece dentro de las 750 horas gratuitas compartidas por
  workspace de Render.

## Estimación

| Concepto | Consumo estimado | Costo mensual estimado |
|---|---:|---:|
| Workspace Render Hobby | 1 workspace | $0 |
| Servicio web Flask | Menos de 750 horas compartidas/mes | $0 |
| Tráfico de salida | [COMPLETAR] MB/mes | $0 dentro de la capa gratuita |
| Base de datos | No implementada | $0 |
| CI | Repositorio público | $0 |
| Total | — | $0 |

## Punto de ruptura de la capa gratuita

La estimación deja de aplicar cuando el workspace supera las 750 horas de
instancia gratuita compartidas durante el mes, cuando se requiere evitar la
suspensión tras 15 minutos de inactividad o cuando se incorpora infraestructura
de pago, como una base de datos persistente.

Una instancia activa durante 31 días consumiría aproximadamente 744 horas.
Por ello, el margen restante para otros servicios gratuitos del mismo workspace
sería reducido.

## Costos no monetarios y riesgos

- Render puede suspender el servicio tras 15 minutos de inactividad.
- La primera solicitud posterior puede tardar mientras el servicio se reactiva.
- La persistencia en memoria pierde los datos ante reinicio, redeploy o caída.
- El equipo debe poder revisar logs, redesplegar y ejecutar el procedimiento de
  reversión.