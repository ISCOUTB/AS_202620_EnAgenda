# Comparación de alternativas de despliegue — API Flask de EnAgenda

## Pieza evaluada

La pieza evaluada es la **API Flask de EnAgenda**, ejecutada como un contenedor
Docker construido desde el `Dockerfile` y orquestado con
`docker-compose.yml`.

## Alternativas

| Alternativa | Rol | Ventajas | Desventajas |
|---|---|---|---|
| Dokploy administrado por la universidad | Elegida | Infraestructura institucional, conexión con GitHub, despliegue desde `master`, uso de `Dockerfile` y `docker-compose.yml`, variables centralizadas, logs y estado de despliegue | Depende de cuotas, dominios, permisos y capacidades de la infraestructura institucional |
| Ejecución manual en servidor institucional con Docker Compose | Descartada / reversión | Usa la misma imagen o archivo Compose, no depende de la interfaz de Dokploy y puede servir como recuperación | Requiere más operación manual, configuración de proxy, puertos, dominio, acceso al servidor y monitoreo |

## Resultado de la alternativa elegida

Dokploy se configuró para usar:

| Elemento | Configuración |
|---|---|
| Repositorio | `ISCOUTB/AS_202620_EnAgenda` |
| Rama | `master` |
| Activación | `On Push` |
| Archivo Compose | `./docker-compose.yml` |
| Puerto interno | `5000` |
| Estado de despliegue | Exitoso |

El despliegue construyó la imagen Docker e inició el contenedor correctamente.

## Conclusión

Se elige Dokploy porque la infraestructura es suministrada por la universidad,
no exige tarjeta personal y admite el contenedor Docker ya definido. La
alternativa manual se conserva como mecanismo de reversión, pero aumenta el
trabajo operativo y la probabilidad de diferencias de configuración.

Render no se compara como alternativa porque no se realizó un despliegue real
en esa plataforma y dejó de ser candidato para el proyecto.