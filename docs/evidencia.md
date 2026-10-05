# Evidencias del Corte Vertical

Este documento reúne las evidencias de instalación, ejecución, pruebas, observabilidad y despliegue del corte vertical implementado para el módulo de Invitaciones de EnAgenda.

El flujo validado atraviesa las siguientes partes de la aplicación:

```text
Interfaz web
    ↓
Flask (app/web.py)
    ↓
GestionarInvitacion
    ↓
Invitacion / EstadoInvitacion
    ↓
RepositorioInvitacionesMemoria
```

## Instalación de dependencias

Desde la raíz del proyecto se instalaron las dependencias definidas en `requerimiento.txt`:

```powershell
python -m pip install -r requerimiento.txt
```

La instalación permitió verificar, entre otras, las siguientes dependencias principales:

```text
pytest 8.4.2
Flask 3.1.3
Jinja2 3.1.6
Werkzeug 3.1.8
```

Las dependencias se instalaron correctamente y quedaron disponibles para la ejecución y las pruebas del proyecto.

## Ejecución local de la aplicación

La aplicación Flask puede iniciarse desde la raíz del repositorio mediante:

```powershell
python app\web.py
```

Durante la validación local, Flask inició correctamente en el puerto `5000`:

```text
* Serving Flask app 'web'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

Esto permitió acceder a la interfaz web y comprobar manualmente el flujo implementado para la gestión de invitaciones.

## Validación del corte vertical de Invitaciones

Se verificó el flujo funcional implementado para el módulo de Invitaciones.

El organizador puede:

1. Definir la cantidad de invitados.
2. Establecer una fecha y hora límite de respuesta.
3. Registrar el nombre y correo electrónico de cada invitado.
4. Crear múltiples invitaciones.
5. Obtener un enlace individual para cada invitado.

Cada invitación genera un token individual que permite acceder a su información.

El invitado puede utilizar el enlace generado para consultar la invitación y registrar su respuesta de asistencia como `Confirmado` o `No asistiré`, respetando las reglas de vigencia definidas por el dominio.

La interfaz utilizada para este flujo está implementada mediante Flask, Jinja2, HTML y CSS.

## Pruebas automatizadas

Después de actualizar el flujo de invitaciones y realizar la integración de los cambios, se ejecutó la suite automatizada mediante:

```powershell
python -m pytest -q
```

Resultado validado:

```text
14 passed
```

Las pruebas incluyen verificaciones relacionadas con:

- Reglas del módulo de Invitaciones.
- Operaciones HTTP de invitaciones.
- Contrato OpenAPI.
- Comportamiento del corte vertical implementado.

El resultado confirma que las pruebas automatizadas existentes finalizaron correctamente después de la integración de los cambios.

## Verificación de salud de la aplicación

La aplicación dispone del endpoint `/health` para comprobar el estado del servicio.

Durante la ejecución local se realizó la consulta:

```powershell
curl.exe -i http://localhost:5000/health
```

Resultado:

```text
HTTP/1.1 200 OK
```

La respuesta indicó que el servicio se encontraba disponible.

## Verificación de métricas

La aplicación también dispone del endpoint `/metrics`.

La consulta local se realizó mediante:

```powershell
curl.exe -i http://localhost:5000/metrics
```

Se obtuvo una respuesta HTTP satisfactoria y se verificó la exposición de métricas relacionadas con la aplicación, entre ellas:

```text
enagenda_invitaciones_consultadas_total
http_requests_total
http_requests_by_path
http_responses_by_status
```

Estas métricas permiten observar solicitudes HTTP y operaciones relacionadas con la consulta de invitaciones.

## Validación local con Docker

Para comprobar que la aplicación podía ejecutarse mediante contenedores, desde la raíz del repositorio se utilizó:

```powershell
docker compose up --build
```

Durante la validación:

```text
La imagen Docker fue construida correctamente.
El contenedor inició correctamente.
La aplicación quedó disponible en el puerto 5000.
```

Posteriormente se verificaron los endpoints `/health` y `/metrics` sobre la aplicación ejecutada mediante Docker.

Para detener los contenedores se puede utilizar:

```powershell
docker compose down
```

## Despliegue en Dokploy

### Configuración del despliegue

El proyecto fue desplegado utilizando la plataforma institucional Dokploy.

| Elemento | Valor |
|---|---|
| Plataforma | Dokploy institucional |
| Proyecto | `enagenda` |
| Entorno | `production` |
| Servicio | `sistema` |
| Repositorio | `ISCOUTB/AS_202620_EnAgenda` |
| Rama | `master` |
| Método de despliegue | Reconstrucción y despliegue desde Dokploy |
| Archivo Compose | `./docker-compose.yml` |
| Puerto interno | `5000` |

El despliegue automático no se considera activo en la configuración documentada actualmente. Después de integrar y enviar cambios a `master`, la composición puede reconstruirse desde Dokploy para obtener la versión actualizada del repositorio.

### Resultado del despliegue

Dokploy obtuvo el código del repositorio, construyó la imagen definida para EnAgenda y levantó la aplicación mediante Docker Compose.

Durante el proceso se registró la construcción e inicio del contenedor:

```text
Image enagenda-sistema-m7pzgi-enagenda Built
Container enagenda-sistema-m7pzgi-enagenda-1 Started
Docker Compose Deployed: ✅
```

La aplicación desplegada permitió acceder a la interfaz web de EnAgenda y continuar la validación del flujo de Invitaciones.

## Integración de la nueva interfaz

La interfaz del módulo de Invitaciones fue desarrollada e integrada desde la rama:

```text
feature/ui-invitaciones
```

Antes de integrarla, la rama `master` fue actualizada con los cambios existentes en el repositorio remoto.

Posteriormente se realizó la integración de la interfaz y se enviaron los cambios a `origin/master`.

La actualización incorporó las vistas y estilos necesarios para representar el flujo de invitaciones, además de conservar los cambios previamente existentes en la aplicación.

El flujo visual contempla:

```text
Configuración de invitaciones
        ↓
Registro de invitados
        ↓
Creación de invitaciones
        ↓
Generación de enlaces individuales
        ↓
Consulta de la invitación
        ↓
Confirmación o rechazo de asistencia
```

## Corrección identificada durante el despliegue

Después de reconstruir la aplicación en Dokploy, la interfaz principal cargó correctamente. Sin embargo, al continuar con el proceso de creación de invitaciones se produjo un error HTTP `500`.

Los logs de la aplicación permitieron identificar:

```text
jinja2.exceptions.TemplateNotFound: invitados.html
```

El error se originaba porque `app/web.py` intentaba renderizar la plantilla `invitados.html`, pero esta no se encontraba disponible dentro de `app/templates/`.

La solución consistió en completar la capa de presentación incorporando:

```text
app/templates/invitados.html
app/static/css/invitados.css
```

No fue necesario modificar las reglas del dominio ni el caso de uso `GestionarInvitacion`, debido a que el problema correspondía a un recurso faltante de la interfaz web.

Esta validación permitió comprobar la importancia de revisar tanto las pruebas automatizadas como el comportamiento real de la aplicación después del despliegue.

## Estado actual de la evidencia

A partir de las verificaciones realizadas se cuenta con evidencia de:

- Instalación correcta de las dependencias.
- Ejecución local de la aplicación Flask.
- Funcionamiento del corte vertical del módulo de Invitaciones.
- Creación múltiple de invitaciones.
- Generación de tokens y enlaces individuales.
- Interfaz web para el flujo de invitaciones.
- Ejecución satisfactoria de las pruebas automatizadas.
- Endpoints de salud y métricas.
- Construcción y ejecución mediante Docker.
- Despliegue de la aplicación mediante Dokploy.
- Integración de la interfaz con la rama `master`.
- Identificación y corrección de un error de plantilla durante la validación del despliegue.

La evidencia obtenida respalda el corte vertical actual del módulo de Invitaciones y su integración dentro de la arquitectura de monolito modular seleccionada para EnAgenda.