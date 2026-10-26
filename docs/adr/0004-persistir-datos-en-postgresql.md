# 0004 — Persistir usuarios, eventos e invitaciones en PostgreSQL

- Estado: Aceptada
- Fecha: 25-Oct-2026
- Alcance: documentar la persistencia ya incorporada en el ZIP y sus límites.

## Contexto

Los usuarios, eventos y respuestas deben sobrevivir reinicios y ser compartidos
por los procesos Flask. El flujo nuevo usa SQLAlchemy, PostgreSQL y migraciones
Alembic. El flujo heredado de invitaciones aún usa memoria y queda fuera de esta
garantía. Véase [arc42 §8](../arc42/08-conceptos-transversales.md).

## Alternativas

| Decisión | Costo de reversión estimado por tareas, no por horas medidas |
|---|---|
| PostgreSQL relacional con claves y migraciones | Alto: transformar tres tablas relacionadas, preservar IDs y tokens, portar tres repositorios y consultas con bloqueo, adaptar migraciones, respaldos, Compose y pruebas; planear corte y restauración. |
| Mantener memoria como fuente principal | Bajo cambio inicial; pierde estado y no coordina workers. Migrar después exige diseñar el esquema y transferir los datos que aún existan. |
| SQLite como base productiva | Menos operación inicial; no proporciona la misma coordinación por fila usada aquí y requiere rediseñar la concurrencia al crecer. |
| Caché / sin caché | Menor costo de reversión: añadir o quitar una capa de lectura sin cambiar la fuente de verdad, pero exige invalidación y medición. |
| Broker / flujo síncrono | Hoy no hay contratos ni consumidores asíncronos persistidos que migrar; introducirlos no es necesario para el alcance. |

## Decisión

Conservar PostgreSQL como fuente de verdad del flujo de eventos. Mantener un
monolito Flask, repositorios SQLAlchemy y cambios de esquema versionados con
Alembic. No introducir caché de negocio ni broker para S12.

La persistencia relacional es la decisión de datos más costosa de revertir ahora:
abarca datos existentes y sus relaciones, contrato de tokens, código de lectura y
escritura, migraciones y operación. A diferencia de añadir una caché, cambiar el
almacén requiere convertir y validar los datos sin perder respuestas ni enlaces.
El desglose anterior es una comparación cualitativa, no una cotización ni medición.

## Consecuencias y reversión

Ganamos durabilidad y transacciones. Debemos administrar credenciales, volumen,
backups y migraciones. Los límites de cupo se coordinan bloqueando usuario o evento;
no deben existir caminos alternativos que omitan esos bloqueos. El flujo heredado
sigue siendo deuda y no se denomina persistente.

Para revertir: respaldar y ensayar restauración; exportar tablas preservando IDs,
tokens y UTC; implementar consultas equivalentes; validar conteos y referencias;
realizar corte de escritura y migración; conservar un plan de retorno probado.
No se ha ejecutado una migración de reversión durante esta revisión.

## Verificación

Pruebas en `tests/test_consistencia_s12.py` validan rollback y límites con SQLite
aislado. No acreditan coordinación multiworker de PostgreSQL. Las pruebas de
concurrencia real, restauración de backups y despliegue siguen pendientes.
