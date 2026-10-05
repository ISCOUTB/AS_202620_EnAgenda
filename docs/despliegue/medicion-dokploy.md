# Medición de reactivación de Render Free

## Contexto

Render Free puede suspender un servicio web después de 15 minutos sin tráfico.
Esta medición evalúa el comportamiento de reactivación de la API Flask de
EnAgenda.

## Procedimiento

1. Se verificó que `GET /health` respondiera correctamente con el servicio
   activo.
2. No se enviaron solicitudes a la URL durante al menos 16 minutos.
3. Se midió la primera solicitud posterior a la inactividad.
4. Se midió una segunda solicitud inmediata.

Comando utilizado:

```bash
curl -s -o /dev/null -w "codigo=%{http_code} tiempo=%{time_total}s\n" \
  https://[URL-REAL].onrender.com/health
```

## Resultados

| Fecha y hora | Condición | Código HTTP | Tiempo total |
|---|---|---:|---:|
| Pendiente | Servicio activo | Pendiente | Pendiente |
| Pendiente | Primera solicitud después de 16 minutos | Pendiente | Pendiente |
| Pendiente | Segunda solicitud inmediata | Pendiente | Pendiente |

## Conclusión

Pendiente de ejecutar la medición sobre el entorno público.