# Auditoría de dependencias — S13

## Alcance

Fecha: 23 de noviembre de 2026.

Se analizaron las versiones instaladas en una imagen local Docker de EnAgenda,
con Python 3.13.18. La herramienta pip-audit 2.10.1 se instaló en un entorno
virtual temporal separado.

El inventario se obtuvo mediante pip freeze antes de instalar la herramienta.
Se analizó con --no-deps y --disable-pip para no resolver versiones diferentes.

Esta revisión cubre avisos conocidos de paquetes Python inventariados.
No es un escaneo del sistema operativo de la imagen, una prueba de penetración
ni un análisis exhaustivo de secretos del historial Git.

## Hallazgo inicial

El reporte original identificó pytest 8.4.2 con dos entradas del mismo aviso:

- PYSEC-2026-1845.
- Alias: CVE-2025-71176 y GHSA-6w46-j5rx-g56g.
- Versión corregida indicada: 9.0.3.

Las entradas duplicadas no se presentan como dos vulnerabilidades distintas.

El aviso describe riesgos por manejo de directorios temporales en UNIX ante
usuarios locales. No demuestra una explotación remota de EnAgenda.

## Decisión y verificación

Se sustituyó pytest>=8.0,<9.0 por pytest==9.0.3 en requerimiento.txt.
No se aplicaron correcciones automáticas indiscriminadas.

Después de reconstruir la imagen:

- Se confirmó pytest 9.0.3.
- Se ejecutaron 54 pruebas, todas aprobadas en 11,47 segundos.
- El proceso de pruebas devolvió código 0.
- Se repitió la auditoría con pip-audit 2.10.1.
- La auditoría devolvió código 0 y No known vulnerabilities found.
- El registro de pytest 9.0.3 contiene una lista vacía de vulnerabilidades.

Estado: corregido y verificado localmente.
Publicación, CI y despliegue de esta actualización se verifican por separado.

## Evidencia

- [Reporte inicial](../evidencias/auditoria-dependencias.json).
- [Inventario inicial](../evidencias/dependencias-auditadas.txt).
- [Reporte posterior](../evidencias/auditoria-pytest-9.json).
- [Inventario posterior](../evidencias/dependencias-pytest-9.txt).
- [Versión de herramienta](../evidencias/version-auditoria-pytest-9.txt).
- [Pruebas posteriores](../evidencias/pruebas-pytest-9.txt).

## Límites y seguimiento

No detectar avisos conocidos no certifica ausencia de vulnerabilidades.

El resto de dependencias se mantiene según requerimiento.txt; esta auditoría
no demuestra que pytest fuera el único paquete cuya versión cambió al
reconstruir. Los inventarios conservan las versiones de ambas ejecuciones.

Pendientes: separar dependencias productivas y de desarrollo, fijar el conjunto
resuelto con hashes y automatizar revisiones periódicas.

No se ha completado una revisión de todos los paquetes del sistema operativo
ni una auditoría exhaustiva del historial por secretos.