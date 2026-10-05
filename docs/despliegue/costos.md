# Estimación de costos de despliegue — Dokploy

## Supuestos

- Una instancia de API Flask para el MVP de EnAgenda.
- La aplicación se ejecuta en un contenedor Docker.
- La persistencia actual está implementada en memoria; no existe una base de
  datos desplegada.
- Dokploy es provisto por la universidad y no genera costo monetario directo
  para el equipo.
- GitHub y el repositorio del proyecto se utilizan para el código fuente y la
  integración continua.
- Los límites de CPU, RAM, almacenamiento, transferencia y disponibilidad deben
  confirmarse con la infraestructura institucional.

## Estimación actual

| Concepto | Supuesto | Costo mensual para el equipo |
|---|---|---:|
| Despliegue de la API | Dokploy institucional | $0 |
| Imagen Docker | Construida desde el repositorio | $0 |
| Repositorio y CI | GitHub y GitHub Actions | $0 |
| Base de datos | No implementada en el MVP actual | $0 |
| Certificado HTTPS | Pendiente de dominio institucional o temporal | $0 estimado |
| Total monetario estimado | — | $0 |

## Punto de ruptura

La estimación deja de ser válida si el equipo supera una cuota institucional de
CPU, memoria, almacenamiento, tráfico o cantidad de servicios, o si incorpora
una base de datos, dominio propio, servicio externo o infraestructura que no
esté cubierta por la universidad.

Los valores concretos se actualizarán cuando el laboratorio o la universidad
confirme las cuotas asignadas al proyecto.