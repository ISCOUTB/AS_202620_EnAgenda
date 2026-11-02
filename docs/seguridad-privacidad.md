# Seguridad y privacidad de EnAgenda

**Fecha de revisión:** 1 de noviembre de 2026  
**Proyecto:** AS_202620_EnAgenda  
**Alcance:** análisis de amenazas, dependencias y tratamiento de datos personales.

## 1. Alcance del análisis

EnAgenda es una aplicación que permite a los organizadores crear eventos, registrar invitados y gestionar sus respuestas mediante invitaciones individuales.

Durante la revisión se identificaron datos como nombres, correos electrónicos, contraseñas protegidas mediante hash, información de eventos y tokens de invitación.

El análisis se realizó sobre el código del repositorio, sus dependencias y la configuración de la aplicación.

## 2. Tabla de amenazas priorizadas

Se utiliza una escala cualitativa de probabilidad e impacto: alta, media y baja.

| ID | Amenaza identificada | Probabilidad | Impacto | Prioridad | Mitigación asignada |
|---|---|---|---|---|---|
| S-01 | Acceso no autorizado a invitaciones mediante la exposición de tokens individuales. | Media | Alta | Alta | Generar tokens aleatorios, evitar publicarlos y permitir su revocación. |
| S-02 | Exposición de nombres y correos electrónicos de los invitados mediante consultas públicas. | Media | Alta | Alta | Limitar la información que devuelven las rutas públicas y proteger los datos personales. |
| S-03 | Robo de sesiones por transmisión de cookies sin protección HTTPS. | Media | Alta | Alta | Activar `FLASK_SECURE_COOKIES=true` en producción y utilizar HTTPS. |
| S-04 | Exposición de claves y secretos de configuración. | Media | Alta | Alta | Utilizar variables de entorno, mantener `.env` fuera de Git y rotar secretos expuestos. |
| S-05 | Ataques automatizados contra el inicio de sesión y las rutas públicas. | Media | Media | Media | Implementar límites de solicitudes y controles contra intentos repetidos. |
| S-06 | Manipulación de respuestas de invitaciones mediante solicitudes no autorizadas. | Media | Alta | Alta | Validar los tokens, mantener la protección CSRF en formularios y revisar las rutas API heredadas. |
| S-07 | Pérdida de información por el uso de almacenamiento temporal en memoria en el flujo heredado. | Alta | Media | Media | Priorizar la persistencia en PostgreSQL y retirar progresivamente el flujo heredado. |
| S-08 | Vulnerabilidades conocidas en bibliotecas de terceros. | Media | Alta | Mitigada | Actualizar las dependencias afectadas y repetir el análisis con `pip-audit`. |

Las amenazas representan riesgos potenciales identificados durante la revisión; no significan que todos hayan ocurrido en el sistema.

## 3. Análisis de dependencias

Se revisó el archivo `requerimiento.txt`, que contiene las dependencias utilizadas por el proyecto:

- pytest: ejecución de pruebas.
- Flask: desarrollo de la aplicación web.
- Schemathesis: pruebas del contrato API.
- Gunicorn: servidor WSGI.
- SQLAlchemy: acceso a bases de datos.
- psycopg: conexión con PostgreSQL.
- Alembic: gestión de migraciones.
- Flask-WTF: protección CSRF.

### 3.1 Herramienta utilizada

Se utilizó `pip-audit` para identificar vulnerabilidades conocidas en las dependencias declaradas y sus dependencias transitivas.

Comando ejecutado:

```powershell
pip-audit -r requerimiento.txt
```

### 3.2 Resultado inicial

La primera auditoría reportó el aviso `PYSEC-2026-1845`, asociado a `pytest 8.4.2`. La versión corregida indicada por la herramienta fue `9.0.3`.

### 3.3 Mitigación aplicada

Se modificó la restricción de pytest en `requerimiento.txt`:

```text
pytest>=9.0.3,<10
```

Posteriormente se instaló `pytest 9.2.0`.

Se ejecutó nuevamente la auditoría y se obtuvo el siguiente resultado:

```text
No known vulnerabilities found
```

**Resultado:** la vulnerabilidad identificada quedó mitigada y el segundo análisis no reportó vulnerabilidades conocidas en las dependencias auditadas.

### 3.4 Verificación de pruebas

Después de actualizar pytest se ejecutó:

```powershell
pytest -q
```

Resultado:

- 12 pruebas aprobadas.
- 2 pruebas fallidas.

Los fallos corresponden a:

1. `test_health_devuelve_estado_ok`: el endpoint `/health` no devuelve el campo `service` esperado por la prueba.
2. `test_metrics_expone_metricas_http`: el endpoint `/metrics` no devuelve la métrica `http_requests_total` esperada por la prueba.

Estos dos fallos ya estaban presentes antes de actualizar pytest, por lo que no se atribuyen a la actualización de la dependencia.

## 4. Privacidad y tratamiento de datos

### 4.1 Datos tratados

EnAgenda maneja diferentes tipos de información:

| Información | Finalidad |
|---|---|
| Nombre y correo del organizador | Identificación y gestión de la cuenta. |
| Contraseña protegida mediante hash | Autenticación del usuario. |
| Nombre y correo de los invitados | Identificación de los destinatarios de las invitaciones. |
| Título, descripción y ubicación del evento | Organización y presentación de los eventos. |
| Token de invitación | Acceso individual para consultar y responder invitaciones. |

### 4.2 Medidas de protección identificadas

- Las contraseñas se almacenan mediante hash utilizando scrypt.
- Los tokens de invitación se generan mediante mecanismos aleatorios seguros.
- Las sesiones utilizan cookies con las opciones `HttpOnly` y `SameSite`.
- La aplicación dispone de protección CSRF mediante Flask-WTF, aunque existe una excepción explícita para una ruta API heredada.
- Los secretos de configuración se obtienen mediante variables de entorno.
- El archivo `.env` está excluido del repositorio.
- Las respuestas de determinadas rutas utilizan `Cache-Control: no-store`.

### 4.3 Recomendaciones de privacidad

1. Evitar exponer nombres, correos y tokens en respuestas públicas o registros.
2. Definir un periodo de conservación de los datos personales.
3. Establecer procedimientos para corregir y eliminar información cuando corresponda.
4. Informar a los organizadores sobre el tratamiento de los datos de sus invitados.
5. Configurar HTTPS y cookies seguras en el entorno de producción.
6. Restringir el acceso a la información almacenada en PostgreSQL.
7. Proteger las copias de seguridad y limitar su acceso.

## 5. Evidencias del repositorio

Los siguientes archivos permiten relacionar el análisis con la implementación:

| Archivo | Evidencia |
|---|---|
| `requerimiento.txt` | Dependencias y versiones utilizadas. |
| `app/web.py` | Rutas, sesiones, configuración de seguridad y protección CSRF. |
| `src/usuarios/aplicacion/registrar_usuario.py` | Registro y protección de contraseñas. |
| `src/usuarios/aplicacion/autenticar_usuario.py` | Autenticación de usuarios. |
| `src/invitaciones/dominio/invitaciones.py` | Generación y gestión de tokens. |
| `src/invitaciones/infraestructura/modelo_invitacion.py` | Datos de las invitaciones. |
| `src/eventos/infraestructura/modelo_evento.py` | Información de los eventos. |
| `.env.example` y `.gitignore` | Configuración y protección de secretos. |
| `docs/arc42/08-conceptos-transversales.md` | Aspectos transversales de la arquitectura. |
| `docs/arc42/11-riesgos-y-deuda-técnica.md` | Riesgos y deuda técnica identificados. |

## 6. Conclusión

El análisis permitió identificar amenazas relacionadas con la exposición de datos personales, el acceso mediante tokens, la configuración de sesiones y las dependencias externas.

Se aplicó una mitigación sobre la vulnerabilidad reportada en pytest mediante su actualización a la versión 9.2.0. La auditoría posterior no encontró vulnerabilidades conocidas.

Las pruebas automatizadas registraron 12 resultados aprobados y 2 fallidos, correspondientes a diferencias entre los resultados esperados y los endpoints de salud y métricas.

Finalmente, se establecieron medidas de mitigación y recomendaciones para fortalecer la seguridad y privacidad de EnAgenda.
