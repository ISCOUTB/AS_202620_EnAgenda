# 7. Vista de despliegue

## Entorno local

En desarrollo, EnAgenda se ejecuta como una aplicación Flask contenida con
Docker.

```text
Desarrollador
    │
    │ http://localhost:5000
    ▼
Docker Compose
    │
    ▼
Contenedor EnAgenda
    │
    ├── Gunicorn
    ├── Aplicación Flask
    ├── Módulo de Invitaciones
    ├── /health
    ├── /metrics
    └── Repositorio en memoria
```

La imagen se construye con el `Dockerfile`. `docker-compose.yml` publica el
puerto `5000` y carga variables desde `.env`. El archivo `.env` se crea a
partir de `.env.example` y no se versiona.

## Entorno institucional

El despliegue del MVP se realiza en Dokploy institucional.

```text
GitHub: ISCOUTB/AS_202620_EnAgenda
    │
    │ push a master
    ▼
Dokploy
    │
    ├── Proyecto: enagenda
    ├── Entorno: production
    ├── Servicio: sistema
    ├── Compose: ./docker-compose.yml
    └── Variables gestionadas en Dokploy
    │
    ▼
Contenedor EnAgenda
    │
    ├── Dockerfile
    ├── Python 3.13 slim
    ├── Gunicorn
    ├── Flask
    ├── Puerto interno 5000
    ├── /health
    └── /metrics
```

Dokploy está conectado al repositorio GitHub en la rama `master` con activación
`On Push`. Cuando se envía un commit a esa rama, Dokploy clona el repositorio,
construye la imagen y ejecuta el servicio definido en `docker-compose.yml`.

## Estado validado

El despliegue institucional fue completado correctamente. Los logs confirmaron:

```text
Image enagenda-sistema-m7pzgi-enagenda Built
Container enagenda-sistema-m7pzgi-enagenda-1 Started
Docker Compose Deployed: ✅
```

## Exposición pública

El servicio se encuentra desplegado, pero el host o URL pública aún debe
configurarse mediante la pestaña **Domains** de Dokploy.

La configuración prevista es:

- Servicio: `enagenda`.
- Puerto interno: `5000`.
- Ruta pública: `/`.
- Ruta interna: `/`.
- HTTPS: pendiente de dominio válido o configuración institucional.

## Validación operativa

La disponibilidad se validará con:

- `GET /health`, que debe responder `HTTP 200`.
- `GET /metrics`, que debe responder `HTTP 200`.
- Revisión de logs en Dokploy.
- Confirmación del estado del contenedor en ejecución.

## Aspectos pendientes

- Host o dominio público.
- Validación externa de `/health` y `/metrics`.
- Configuración de HTTPS o certificado.
- Límites institucionales de CPU, RAM, almacenamiento y tráfico.
- Mecanismo de rollback habilitado para el equipo.