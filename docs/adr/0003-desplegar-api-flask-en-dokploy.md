# 0003 — Desplegar la API Flask en Dokploy

- Estado: Aceptada
- Fecha: 04-Oct-2026

## Contexto

EnAgenda requiere un mecanismo reproducible de despliegue para el MVP. La
aplicación se ejecuta como una API Flask contenida en Docker, definida mediante
el `Dockerfile` y `docker-compose.yml` versionados en el repositorio.

No se realizó un despliegue real en Render. Por tanto, Render no representa una
plataforma aplicada ni un candidato vigente para esta decisión.

El equipo cuenta con acceso al proyecto institucional `enagenda`, en el entorno
`production` de Dokploy. El servicio configurado se denomina `sistema`, está
conectado al repositorio GitHub `ISCOUTB/AS_202620_EnAgenda`, usa la rama
`master` y se activa mediante `On Push`.

Dokploy ejecuta el archivo `./docker-compose.yml`. El despliegue construye la
imagen a partir del `Dockerfile`, instala dependencias desde
`requerimiento.txt` e inicia el contenedor de EnAgenda.

## Alternativas consideradas

### A. Dokploy administrado por la universidad

**A favor**

- La infraestructura es proporcionada por el curso o la universidad.
- No exige tarjeta personal ni cuenta personal de pago.
- Está conectado al repositorio GitHub del equipo.
- Ejecuta el archivo `docker-compose.yml` y construye la imagen desde el
  `Dockerfile`.
- Centraliza las variables de entorno del servicio.
- Registra despliegues, logs y estado del contenedor.
- Puede exponer el contenedor mediante un dominio o URL pública.

**En contra**

- El equipo depende de la infraestructura institucional, sus dominios,
  permisos, cuotas y mecanismos disponibles.
- Los límites de CPU, memoria, almacenamiento, tráfico y disponibilidad no han
  sido confirmados.
- La reversión depende del historial y las capacidades habilitadas en Dokploy.
- La URL pública y HTTPS aún deben configurarse mediante un host válido.

### B. Servidor institucional administrado manualmente

**A favor**

- Permite ejecutar la misma imagen Docker o `docker compose`.
- Es independiente de la interfaz específica de Dokploy.
- Puede utilizarse como mecanismo de recuperación si no existe rollback
  disponible en Dokploy.

**En contra**

- Requiere más trabajo operativo.
- Requiere administrar acceso, proxy, puertos, dominio, logs y operación del
  servidor.
- Aumenta la probabilidad de diferencias de configuración entre ambientes.

## Decisión

Se adopta Dokploy, provisto por la universidad, como plataforma de despliegue
del MVP de EnAgenda.

La API Flask se construye desde el `Dockerfile` versionado en el repositorio y
se ejecuta mediante `./docker-compose.yml`. Las variables sensibles se
configuran en Dokploy y no se almacenan en el repositorio.

La elección responde a la restricción de no exigir cuentas personales de pago
ni tarjetas y permite mantener el despliegue integrado con GitHub y Docker.

## Evidencia de aplicación

El servicio fue desplegado correctamente desde Dokploy con el commit de la rama
`master` correspondiente a la actualización de Render a Dokploy.

Los logs de Dokploy registraron:

```text
Image enagenda-sistema-m7pzgi-enagenda Built
Container enagenda-sistema-m7pzgi-enagenda-1 Started
Docker Compose Deployed: ✅
```

## Consecuencias

- El repositorio conserva `Dockerfile`, `docker-compose.yml`, `.dockerignore`
  y `.env.example`.
- El puerto interno de la aplicación es `5000`.
- `.env` permanece fuera del repositorio.
- Dokploy utiliza la rama `master` y se activa mediante `On Push`.
- `/health` y `/metrics` se usarán para comprobar la disponibilidad cuando se
  configure la URL pública.
- La URL pública, el dominio, HTTPS, cuotas de recursos y el mecanismo de
  rollback deben documentarse cuando sean confirmados por la infraestructura.