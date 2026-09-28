# Procedimiento de despliegue y reversión

## Requisitos

- Repositorio clonado.
- Docker Desktop o Docker Engine para la validación local.
- Archivo `.env` creado a partir de `.env.example`.
- Acceso a Render.
- Variable `SECRET_KEY` configurada únicamente en el entorno de Render.

## Preparar el entorno local

Desde la raíz del repositorio:

```bash
cp .env.example .env
```

En Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Editar `.env` y definir una clave local de desarrollo.

## Ejecutar y verificar localmente

```bash
docker compose up --build
```

En otra terminal:

```bash
curl -i http://localhost:5000/health
curl -i http://localhost:5000/metrics
pytest -q
```

Para detener:

```bash
docker compose down
```

## Despliegue en Render

1. Hacer push del código a la rama `main`.
2. Confirmar que el workflow de GitHub Actions finalice en verde.
3. Crear un servicio mediante el archivo `render.yaml`.
4. Seleccionar el plan gratuito.
5. Configurar `SECRET_KEY` en las variables de entorno de Render.
6. Esperar a que Render construya y despliegue el contenedor.
7. Verificar las URL públicas:
   - `/`
   - `/health`
   - `/metrics`
8. Revisar en Render un log JSON generado por una solicitud.

## Verificación externa

Se debe abrir la URL desde una red diferente a la de la universidad, por ejemplo
datos móviles o una red doméstica. Se verifica que `GET /health` y
`GET /metrics` respondan HTTP 200.

## Reversión al servidor del laboratorio

1. Identificar el último commit estable.
2. Clonar el repositorio en el servidor del laboratorio.
3. Crear un archivo `.env` únicamente en el servidor.
4. Ejecutar:

   ```bash
   docker compose up -d --build
   ```

5. Configurar el puerto o proxy público que indique el laboratorio.
6. Verificar `GET /health`, `GET /metrics` y `pytest -q`.
7. Actualizar README y evidencia con la nueva URL pública.