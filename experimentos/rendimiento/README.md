# S14 — Medición local de invitaciones persistentes

## Objetivo y alcance

Comprobar tiempos y errores del recorrido HTTP:

GET de invitación → POST de respuesta → GET de verificación.

Ruta: /eventos/invitacion/<token>.
Persistencia: PostgreSQL.
CSRF habilitado; sesión HTTP independiente por usuario simulado.
Se comprueba el estado mostrado después del POST y en la consulta posterior.

El criterio de esta prueba es p95 menor que 2000 ms por operación,
sin errores HTTP, de transporte ni de validación del resultado.

## Entorno

- Fecha: 23-Nov-2026.
- Código de aplicación de referencia: a460d9c.
- Rama de trabajo: test/s14-rendimiento.
- Docker Compose local sobre Docker Desktop en Windows.
- Aplicación con Gunicorn 23.0.0 y un worker sync, según el log de arranque.
- PostgreSQL 17; esquema preparado mediante Alembic.
- Generador ejecutado en un contenedor separado del mismo proyecto Compose.
- Destino interno: http://enagenda:5000.
- Evento ficticio 2 y diez invitaciones distintas.
- El script de medición y sus resultados se incorporan después del commit
  de aplicación indicado; no se afirma que ya estuvieran en ese commit.

## Método

- Etapas secuenciales de 1, 5 y 10 usuarios simulados.
- Una invitación distinta por usuario concurrente.
- 20 recorridos por usuario y etapa.
- Diez recorridos de calentamiento excluidos.
- Pausa de 0,1 segundos entre recorridos de cada usuario.
- Modelo cerrado: cada usuario espera a completar su recorrido antes
  de iniciar el siguiente; no se fija una tasa de llegada.
- Respuestas alternadas entre confirmado y no_asistire.
- p95 calculado mediante rango más cercano.
- 320 recorridos y 960 peticiones medidas.
- El tiempo del recorrido excluye la pausa entre recorridos.

## Resultados

Tiempos en milisegundos.

| Usuarios | Recorridos | p95 consultar | p95 responder | p95 verificar | p95 recorrido | Errores |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 20 | 13.609 | 55.518 | 12.629 | 76.786 | 0 |
| 5 | 100 | 30.307 | 49.800 | 35.986 | 127.066 | 0 |
| 10 | 200 | 46.737 | 64.158 | 57.670 | 160.372 | 0 |

Código de salida: 0.

El criterio definido se cumplió en las tres etapas.
El máximo del recorrido con diez usuarios fue 211.751 ms.

## Evidencia

- [Resumen JSON](../../docs/evidencias/s14-local-20261123T163339Z/resumen.json).
- [Peticiones CSV](../../docs/evidencias/s14-local-20261123T163339Z/peticiones.csv).
- [Script](s14_rendimiento.py).

## Ejecución

Requiere aplicación local en ejecución, esquema compatible y evento 2
identificado con un título que empiece por S14, con diez invitados de prueba.
El script modifica sus respuestas. No utilizar sobre datos reales.

Desde PowerShell, en la raíz del repositorio:

```powershell
$commitS14 = git rev-parse HEAD

docker compose run --rm --no-deps `
  -e PYTHONPATH=/app `
  -e S14_CONFIRMAR=EVENTO_2_LOCAL `
  -e "S14_COMMIT=$commitS14" `
  -v "${PWD}:/evidencia" `
  enagenda python /evidencia/experimentos/rendimiento/s14_rendimiento.py

$LASTEXITCODE
```

## Límites

Esta es una ejecución breve, local y de un solo recorrido de negocio.
No incluye renderizado de navegador, descarga de estáticos, Internet,
proxy público, autenticación del organizador ni otros módulos.

El generador comparte recursos del equipo con los servicios.
No se midieron consumo de CPU/RAM, capacidad máxima ni resistencia prolongada.
La verificación funcional lee el formulario devuelto por la aplicación;
no constituye un ensayo de restauración o durabilidad ante caída.

Se aporta evidencia parcial para EC-05, no una certificación completa de
rendimiento productivo ni el cierre total de S14.