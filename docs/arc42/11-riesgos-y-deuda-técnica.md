# 11. Riesgos y Deuda Técnica

Esta sección identifica los principales riesgos técnicos y arquitectónicos
de EnAgenda, así como las decisiones o limitaciones que pueden generar deuda
técnica durante el desarrollo del proyecto.

## 11.1 Riesgos arquitectónicos

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| RA-01 | Los límites entre módulos pueden no respetarse y generar acoplamiento innecesario. | Media | Alta | Mantener cada módulo organizado por dominio, aplicación e infraestructura y evitar el acceso directo a detalles internos de otros módulos. |
| RA-02 | La implementación real puede diferir de la arquitectura documentada. | Media | Alta | Revisar periódicamente la correspondencia entre documentación, código y pruebas, actualizando la arquitectura cuando exista evidencia de cambios. |
| RA-03 | Las reglas de privacidad y vigencia de invitaciones pueden quedar parcialmente implementadas. | Media | Alta | Centralizar las reglas de vigencia y estado en el dominio de Invitaciones y cubrirlas mediante pruebas. |
| RA-04 | El crecimiento de funcionalidades puede aumentar innecesariamente la complejidad del monolito. | Media | Media | Mantener el alcance del MVP y crear nuevas abstracciones o módulos únicamente cuando exista una necesidad comprobada. |
| RA-05 | La solución puede depender demasiado de servicios o herramientas gratuitas con límites de capacidad. | Media | Media | Seleccionar servicios considerando límites de uso, facilidad de reemplazo y costo. Documentar las dependencias externas que finalmente se utilicen. |

## 11.2 Riesgos relacionados con seguridad y privacidad

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| RS-01 | Un invitado podría acceder a información que corresponde a otra invitación. | Baja | Alta | Utilizar identificadores no predecibles y validar el alcance de cada invitación antes de permitir operaciones. |
| RS-02 | Una invitación vencida podría continuar permitiendo operaciones. | Baja | Alta | Comprobar la fecha y hora límite antes de consultar o modificar una invitación. |
| RS-03 | Credenciales o secretos podrían ser incluidos accidentalmente en el repositorio público. | Baja | Alta | Utilizar variables de entorno, excluir archivos sensibles del control de versiones y utilizar únicamente datos ficticios. |

## 11.3 Riesgos relacionados con consistencia

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| RC-01 | Una invitación podría terminar representada por más de una respuesta vigente. | Media | Alta | Mantener un único estado vigente por invitación y realizar pruebas de creación y actualización. |
| RC-02 | Los conteos del panel podrían no coincidir con los estados actuales de las invitaciones. | Media | Alta | Calcular los conteos a partir del estado vigente de cada invitación y validar el resultado mediante pruebas. |

## 11.4 Riesgos relacionados con el desarrollo

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| RD-01 | El equipo de tres estudiantes puede disponer de tiempo limitado para implementar todas las funcionalidades previstas. | Alta | Alta | Priorizar el MVP y desarrollar primero las funcionalidades esenciales: eventos, invitaciones y respuestas de asistencia. |
| RD-02 | La documentación puede adelantarse a funcionalidades que todavía no están implementadas. | Media | Media | Diferenciar claramente entre arquitectura prevista e implementación comprobada y actualizar las secciones a medida que avance el código. |
| RD-03 | Los cambios realizados por diferentes integrantes pueden generar conflictos o inconsistencias entre módulos. | Media | Media | Mantener límites claros entre módulos, revisar cambios y comprobar las pruebas antes de integrar funcionalidades. |

## 11.5 Deuda técnica actual

La deuda técnica identificada en el estado actual del proyecto es principalmente
de documentación e implementación parcial.

### DT-01 — Implementación parcial de módulos

La arquitectura contempla módulos para eventos, invitaciones, tareas,
agenda, presupuesto y panel. Sin embargo, la implementación comprobable
actualmente se concentra principalmente en el módulo de Invitaciones.

**Consecuencia:** existe una diferencia entre la arquitectura prevista para
el MVP y el nivel de implementación actual.

**Plan:** implementar progresivamente los módulos restantes y actualizar las
vistas de arquitectura cuando exista código que permita comprobar sus
responsabilidades.

### DT-02 — Persistencia en memoria

El módulo de Invitaciones utiliza actualmente
`RepositorioInvitacionesMemoria` para almacenar información.

**Consecuencia:** la información almacenada en memoria no representa todavía
una solución de persistencia adecuada para un despliegue real.

**Plan:** reemplazar posteriormente la implementación en memoria por un
mecanismo de persistencia apropiado para el MVP, manteniendo separadas las
reglas del dominio y la infraestructura.

### DT-03 — Vista de despliegue pendiente

La vista de despliegue de arc42 todavía no contiene la descripción definitiva
del entorno utilizado.

**Consecuencia:** todavía no existe una correspondencia completa entre la
arquitectura lógica y el entorno real de ejecución.

**Plan:** completar esta sección cuando se defina y compruebe el mecanismo
de despliegue del proyecto.

### DT-04 — Pruebas y medición de rendimiento pendientes

El requisito EC-05 establece un objetivo de rendimiento de menos de 2 segundos
para el percentil 95 de las operaciones principales bajo una carga inicial de
hasta 10 usuarios concurrentes.

**Consecuencia:** el objetivo está definido, pero la medición depende de que
exista una implementación suficientemente completa para realizar la prueba.

**Plan:** ejecutar una prueba de carga cuando las operaciones principales estén
implementadas y documentar los resultados obtenidos.

## 11.6 Priorización

Los riesgos que deben recibir mayor atención durante el desarrollo son:

1. **Privacidad y control de acceso de las invitaciones.**
2. **Vigencia de los enlaces individuales.**
3. **Consistencia del estado de las invitaciones y del panel.**
4. **Respeto de los límites entre módulos.**
5. **Diferencia entre la arquitectura documentada y la implementación real.**
6. **Evolución desde persistencia en memoria hacia una persistencia adecuada.**

Estos riesgos se revisarán a medida que avance la implementación y podrán
modificarse cuando exista nueva evidencia técnica.


## Actualización S12 — 25-Oct-2026

La deuda de persistencia está parcialmente resuelta: usuarios, eventos e
invitaciones de `/eventos` usan PostgreSQL. Permanece el flujo heredado en memoria,
con pérdida al reiniciar y tokens distintos; falta consolidarlo o retirarlo con
compatibilidad explícita. Dokploy ya está seleccionado; sustituye la descripción
anterior de selección de despliegue pendiente. Falta verificar el despliegue de
esta revisión, respaldos y concurrencia en PostgreSQL. No hay caché de negocio.

Pendientes transversales: análisis y Quality Gate públicos de SonarCloud;
restauración y trazabilidad histórica de ADR-0003 Render/Dokploy sin reutilizar
números; escaneo redactado del historial completo por credenciales; evidencia de
contribución real de los integrantes. Este paquete no afirma haberlos completado.

## 11.7 Revisión de fallos parciales — 23-Nov-2026

### Alcance y evidencia

La integración productiva prevista sigue el recorrido navegador → Flask →
servicios de aplicación → SQLAlchemy → PostgreSQL. El proveedor de envío del
taller es simulado y no forma parte de este recorrido.

Se ejecutaron conjuntamente 35 pruebas de aplicación y prototipo, con resultado
satisfactorio. La evidencia está en
[pruebas integradas](../evidencias/pruebas-integradas.txt).
Esto no demuestra disponibilidad pública, tolerancia a fallos de red ni
concurrencia real entre procesos PostgreSQL.

### Modos de fallo y mitigaciones

| Modo | Efecto esperado o riesgo | Mitigación y estado | Verificación y pendiente |
|---|---|---|---|
| PostgreSQL no responde | Las operaciones que requieren datos persistentes no pueden completarse. No se debe presentar una escritura fallida como guardada. | Las transacciones delimitan las escrituras. Pendiente comprobar límites de espera, manejo de errores y respuesta visible al usuario ante indisponibilidad real. | Las pruebas de rollback no sustituyen una caída de PostgreSQL. Pendiente ensayo controlado de indisponibilidad y recuperación. |
| PostgreSQL responde tarde o hay contención | La solicitud puede quedar esperando; si el cliente pierde la respuesta, puede desconocer si hubo commit. | Consultar el estado antes de repetir operaciones ambiguas. No se afirma disponer de timeouts específicos ni reintentos automáticos verificados. | Pendiente medir esperas, revisar configuración y probar contención real en PostgreSQL. |
| Una solicitud HTTP llega dos veces | Puede repetirse un alta o un cambio de estado. | Repetir la misma respuesta de asistencia conserva el estado final. El alta repetida de un correo se rechaza en el servicio de invitados. Crear eventos y tareas no tiene clave de idempotencia y puede producir duplicados. | Las pruebas S12 cubren respuesta repetida y duplicados de invitados. Pendiente deduplicación de altas de eventos y tareas. |
| Flask deja de responder | La interfaz y los servicios del monolito quedan indisponibles; la persistencia no implica disponibilidad de la aplicación. | Los datos del flujo PostgreSQL están separados del proceso Flask. Se comprobó manualmente conservación de tareas tras reiniciar la aplicación. | No se ha probado caída abrupta durante commit, recuperación automática ni restauración de un respaldo. El flujo heredado en memoria no comparte esta garantía. |
| El proveedor simulado falla o recibe duplicados | El trabajo puede reintentarse, ignorarse como duplicado o terminar en fallidos dentro del experimento. | El prototipo implementa deduplicación, proveedor simulado idempotente y tres intentos con backoff virtual. No está integrado al MVP. | Once pruebas del taller aprobadas. No acreditan proveedor real, durabilidad ni recuperación después de aceptación remota. |

### Idempotencia y transacciones

La idempotencia se analiza por operación, no como propiedad global del sistema.

- Responder una invitación con el mismo estado conserva el resultado final.
- Repetir un alta de invitado con el mismo correo no debe crear otra fila.
- Crear eventos y tareas puede generar registros distintos si se repite la
  solicitud; queda como deuda de deduplicación.
- El simulador conserva message_id y envio_id para controlar duplicados,
  pero su registro se pierde al finalizar el proceso.
- No se implementa una saga: el flujo persistente actual utiliza transacciones
  locales, sin una secuencia de escrituras coordinadas entre servicios
  independientes. El experimento no acredita atomicidad BD/publicación.

Véanse las garantías y límites en
[conceptos transversales](08-conceptos-transversales.md).

### Decisión de extracción

Se propone mantener Invitaciones dentro del monolito y conservar el simulador
fuera del flujo productivo. La comparación, consecuencias y condiciones de
revisión están en el
[ADR-0005](../adr/0005-mantener-invitaciones-en-monolito.md).

### Deuda actualizada

Tareas ya cuenta con persistencia PostgreSQL y verificación funcional manual.
Las 35 pruebas registradas no incluyen pruebas automatizadas específicas de
Tareas ni certifican toda la seguridad del sistema.

Continúan pendientes: fallos reales de infraestructura, concurrencia en
PostgreSQL, restauración de respaldos, medición de rendimiento, comprobación
del despliegue público y consolidación del flujo heredado en memoria.