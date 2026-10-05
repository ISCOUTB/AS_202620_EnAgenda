# Medición de disponibilidad y latencia — Dokploy

## Estado actual

El contenedor de EnAgenda fue desplegado exitosamente en Dokploy institucional.
La medición externa está pendiente porque aún no se ha creado o asignado una URL
pública mediante un host válido.

## Escenario asociado

EC-XX — Consulta pública de invitación.

## Objetivo

Comprobar que el endpoint de salud de EnAgenda esté disponible desde la URL
pública configurada en Dokploy y que su latencia cumpla el umbral de calidad
aprobado por el equipo.

## Umbral

El endpoint `GET /health` debe responder `HTTP 200` en menos de
`[umbral aprobado] ms` en condiciones normales de operación.

El valor definitivo del umbral se definirá con el escenario de calidad aprobado
por el equipo.

## Procedimiento

1. Configurar en Dokploy una URL pública real o temporal mediante un host
   válido.
2. Realizar un redeploy del servicio después de guardar el dominio.
3. Ejecutar 20 solicitudes consecutivas a:
   `http://[host-asignado]/health` o
   `https://[host-asignado]/health`.
4. Registrar por solicitud el código HTTP y el tiempo total de respuesta.
5. Guardar los resultados en un archivo CSV o tabla de evidencia.
6. Calcular p50, p95 y el tiempo máximo.
7. Comparar p95 contra el umbral aprobado.
8. Registrar fecha, commit desplegado, host utilizado y resultado.

## Evidencia de despliegue disponible

Dokploy registró:

```text
Image enagenda-sistema-m7pzgi-enagenda Built
Container enagenda-sistema-m7pzgi-enagenda-1 Started
Docker Compose Deployed: ✅
```

## Información pendiente

- Host o URL pública configurada.
- Resultado de `/health` desde internet.
- Resultado de `/metrics` desde internet.
- Umbral de latencia aprobado.
- Cuotas institucionales de recursos.
- Mecanismo de rollback disponible en Dokploy.