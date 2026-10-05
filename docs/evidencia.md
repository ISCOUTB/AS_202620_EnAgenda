#Evidencias de Corte Vertical 


## Intalacion de Dependencias
```text
PS C:\Users\Jeimy Mendez A\Documents\Uni\Arq_Software\AS_202620_EnAgenda> python -m pip install -r requerimiento.txt
Requirement already satisfied: pytest<9.0,>=8.0 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from -r requerimiento.txt (line 1)) (8.4.2)
Requirement already satisfied: Flask==3.1.3 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from -r requerimiento.txt (line 2)) (3.1.3)
Requirement already satisfied: blinker>=1.9.0 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (1.9.0)
Requirement already satisfied: click>=8.1.3 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (8.5.0)
Requirement already satisfied: itsdangerous>=2.2.0 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (2.2.0)
Requirement already satisfied: jinja2>=3.1.2 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (3.1.6)
Requirement already satisfied: markupsafe>=2.1.1 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (3.0.3)
Requirement already satisfied: werkzeug>=3.1.0 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (3.1.8)
Requirement already satisfied: colorama>=0.4 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from pytest<9.0,>=8.0->-r requerimiento.txt (line 1)) (0.4.6)
Requirement already satisfied: iniconfig>=1 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from pytest<9.0,>=8.0->-r requerimiento.txt (line 1)) (2.3.0)
Requirement already satisfied: packaging>=20 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from pytest<9.0,>=8.0->-r requerimiento.txt (line 1)) (26.3)
Requirement already satisfied: pluggy<2,>=1.5 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from pytest<9.0,>=8.0->-r requerimiento.txt (line 1)) (1.6.0)
Requirement already satisfied: pygments>=2.7.2 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from pytest<9.0,>=8.0->-r requerimiento.txt (line 1)) (2.21.0)
```


## Puebas ejecutables desde el terminal
```text
## Pruebas ejecutables desde el terminal
```text
PS C:\Users\Jeimy Mendez A\Documents\Uni\Arq_Software\AS_202620_EnAgenda> pytest -q
............                                                                 [100%]
12 passed in 4.11s

## Ejecucion de Aplicacion
```text
PS C:\Users\Jeimy Mendez A\Documents\Uni\Arq_Software\AS_202620_EnAgenda> python app\web.py
 * Serving Flask app 'web'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 144-640-716
 ```

## Evidencia de despliegue y observabilidad

La aplicación fue ejecutada y verificada mediante comandos locales, permitiendo evidenciar paso a paso el proceso de ejecución, despliegue y comprobación de los servicios.

### Verificación de salud de la aplicación

```text
PS C:\Users\Jeimy Mendez A\Documents\Uni\Arq_Software\AS_202620_EnAgenda> Invoke-WebRequest http://127.0.0.1:5000/health -UseBasicParsing

StatusCode : 200
Content    : {
               "status": "ok"
             }

## Validación local con Docker — 04-Oct-2026

### Construcción y ejecución local

Desde la raíz del repositorio se ejecutó:

```powershell
docker compose up --build
```

Resultado validado:

```text
La imagen Docker fue construida.
El contenedor inició correctamente.
Gunicorn quedó escuchando en el puerto 5000.
```

### Health check local

```powershell
curl.exe -i http://localhost:5000/health
```

Resultado:

```text
HTTP/1.1 200 OK
```

```json
{
  "service": "enagenda-api",
  "status": "ok"
}
```

### Métricas locales

```powershell
curl.exe -i http://localhost:5000/metrics
```

Resultado:

```text
HTTP/1.1 200 OK
```

La respuesta expone:

```text
enagenda_invitaciones_consultadas_total
http_requests_total
http_requests_by_path
http_responses_by_status
```

### Pruebas automatizadas

```powershell
python -m pytest -q
```

Resultado esperado y validado:

```text
14 passed
```

## Despliegue en Dokploy — 04-Oct-2026

### Configuración institucional

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
| Puerto interno | `5000` |

### Resultado del despliegue

Dokploy clonó el repositorio, construyó la imagen Docker e inició el
contenedor. Los logs registraron:

```text
Image enagenda-sistema-m7pzgi-enagenda Built
Container enagenda-sistema-m7pzgi-enagenda-1 Started
Docker Compose Deployed: ✅
```

El panel de Dokploy mostró el estado `Done` para el despliegue del commit
correspondiente a la adaptación de Render a Dokploy.

### Pendiente

- Crear o asignar un host válido en Dokploy.
- Validar la URL pública.
- Validar `/health` y `/metrics` desde internet.
- Configurar HTTPS cuando exista un dominio válido.