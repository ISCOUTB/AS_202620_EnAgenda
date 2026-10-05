# Procedimiento de despliegue — EnAgenda en Dokploy

## Configuración confirmada

| Elemento | Valor |
|---|---|
| Plataforma | Dokploy institucional |
| Proyecto | `enagenda` |
| Entorno | `production` |
| Servicio | `sistema` |
| Repositorio | `ISCOUTB/AS_202620_EnAgenda` |
| Rama | `master` |
| Activación | `On Push` |
| Archivo Compose | `./docker-compose.yml` |
| Puerto interno de la aplicación | `5000` |

## Prerrequisitos

- Acceso al proyecto EnAgenda en Dokploy.
- Repositorio GitHub actualizado.
- Pruebas automatizadas aprobadas localmente.
- `Dockerfile`, `docker-compose.yml`, `.dockerignore` y `.env.example`
  disponibles en el repositorio.
- Variables de entorno configuradas en Dokploy.
- `.env` ausente del repositorio.

## Despliegue en Dokploy

1. Ejecutar las pruebas automatizadas:

   ```powershell
   python -m pytest -q
   ```

2. Verificar los cambios del repositorio:

   ```powershell
   git status
   ```

3. Crear un commit con los cambios validados.

4. Enviar el commit a la rama `master`:

   ```powershell
   git push origin master
   ```

5. Dokploy detecta el cambio mediante la activación `On Push`.

6. Dokploy clona el repositorio y ejecuta:

   ```text
   docker compose -p [nombre-del-servicio] --env-file .env \
   -f ./docker-compose.yml up -d --build --remove-orphans
   ```

7. Confirmar en la pestaña **Deployments** que el estado sea `Done`.

8. Revisar los logs del despliegue y confirmar que aparezcan mensajes de imagen
   construida y contenedor iniciado.

9. Confirmar en la pestaña **Containers** que el contenedor esté en ejecución.

10. Cuando se configure un host, asociarlo al servicio `enagenda`, usar el
    puerto interno `5000`, la ruta `/` y mantener HTTPS desactivado hasta contar
    con un dominio válido y configuración de certificado.

11. Después de crear o cambiar el dominio, realizar un nuevo despliegue.

12. Validar la aplicación por URL pública:

    ```text
    GET /health
    GET /metrics
    GET /
    ```

## Variables de entorno

Las variables se configuran en Dokploy, no en el repositorio. Como mínimo:

```text
PORT=5000
LOG_LEVEL=INFO
SECRET_KEY=[valor secreto configurado en Dokploy]
```

No se debe publicar el valor de `SECRET_KEY` en archivos, commits, evidencias,
capturas o documentación.

## Validación local previa

Antes de enviar cambios a Dokploy:

```powershell
docker compose up --build
curl.exe -i http://localhost:5000/health
curl.exe -i http://localhost:5000/metrics
python -m pytest -q
```

## Reversión

1. Identificar el último commit estable y el último despliegue saludable en la
   pestaña **Deployments** de Dokploy.
2. Usar el historial de despliegues o el mecanismo de redeploy disponible en
   Dokploy, si está habilitado.
3. Si la plataforma no permite rollback, restaurar el último commit estable en
   `master` y hacer `push`.
4. Si se requiere una recuperación manual, ejecutar el `Dockerfile` y
   `docker-compose.yml` en un servidor institucional.
5. Configurar las variables de entorno en el destino.
6. Validar `/health`, `/metrics` y las pruebas automatizadas.