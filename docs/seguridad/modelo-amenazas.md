# Modelo de amenazas y privacidad — S13

Fecha: 23 de noviembre de 2026.
Estado: revisión inicial basada en código, pruebas y comprobaciones disponibles.
No constituye una certificación de seguridad.

## 1. Alcance, activos y actores

Activos:
- Cuentas, hashes de contraseñas y sesiones.
- Eventos, invitados, respuestas y tareas.
- Tokens de invitación y token de observabilidad.
- Credenciales de PostgreSQL, SECRET_KEY y respaldos.
- Código, historial Git y configuración del pipeline.

Actores:
- Organizador autenticado.
- Invitado que posee un enlace individual.
- Visitante no autenticado.
- Organizador que intenta acceder a recursos ajenos.
- Operador con acceso a GitHub, Dokploy o la base de datos.
- Tercero con acceso a la red o a un enlace divulgado.

## 2. Componentes y límites de confianza

Correspondencia lógica para contrastar con C4:

| Elemento | Referencia | Límite relevante |
|---|---|---|
| Organizador e invitado | C4 nivel 1 | Navegador no confiable frente al servidor. |
| Aplicación Flask | C4 nivel 2; componentes del nivel 3 | Valida autenticación, autorización y entradas. |
| PostgreSQL | Unidad de almacenamiento del despliegue | Solo los servicios autorizados deben modificar datos. |
| GitHub Actions y Dokploy | Vista de despliegue | Código, dependencias y secretos de operación. |
| Simulador de mensajería | Experimento separado | No es proveedor ni servicio productivo integrado. |

Diagramas:
- [Contexto](../c4/nivel-1-contexto.md).
- [Contenedores](../c4/nivel-2-contenedores.md).
- [Componentes](../c4/nivel-3-componentes.md).

Esta tabla no certifica que todos los diagramas estén actualizados.
Debe corregirse cualquier diferencia entre sus elementos y el despliegue real.

Flujos sensibles:
1. Registro, login y configuración de cuenta.
2. Administración de eventos, invitados y tareas.
3. Consulta y respuesta mediante token.
4. Consulta de métricas mediante Bearer.
5. Despliegue, migraciones y respaldo.

## 3. Criterio de prioridad

Probabilidad e impacto son estimaciones cualitativas, no frecuencias medidas.
P1: atención inmediata. P2: siguiente incremento de seguridad.

Los responsables son roles propuestos; el equipo debe asignar personas.
"Pendiente" no significa riesgo aprobado ni control implementado.

## 4. Amenazas, controles y evidencia

| ID | Componente y amenaza | Probabilidad / impacto | Prioridad | Control y estado | Evidencia / pendiente | Responsable propuesto |
|---|---|---|---|---|---|---|
| AM-01 | Navegador → Flask: exposición de credenciales o sesión por HTTP. | Media / Alto | P1 | Pendiente verificar HTTPS y configurar cookies Secure en ese entorno. | Se observó acceso HTTP. No afirmar cifrado de transporte. | Operación |
| AM-02 | Flask: un organizador consulta o modifica recursos ajenos. | Media / Alto | P1 | Comprobado parcialmente mediante validación de propietario. | Prueba S12 de propietario, pruebas de cierre ajeno y comprobación manual de Tareas. Falta cobertura completa de rutas y métodos. | Backend |
| AM-03 | Flask: cambios no autorizados mediante CSRF. | Media / Alto | P1 | CSRFProtect configurado; verificación parcial. | test_login_csrf_y_no_store aprobado. Revisar formularios, excepciones y métodos restantes. | Backend |
| AM-04 | Invitaciones: uso de token divulgado o vencido. | Media / Alto | P1 | Pruebas de rechazo de token inexistente y vencido aprobadas. | Pendientes revocación explícita y revisión integral de exposición en URLs y logs. Quien posee un token vigente tiene acceso al alcance autorizado. | Backend |
| AM-05 | Métricas: lectura no autorizada o filtración de tokens. | Media / Medio | P2 | Bearer validado; 401 ante acceso inválido; 503 sin secreto. | Pruebas de métricas y exclusión de tokens aprobadas. Esto no certifica todos los logs ni agregación multiworker. | Backend / operación |
| AM-06 | Cadena de suministro: dependencia con aviso conocido. | Media / Alto | P1 | pytest actualizado a 9.0.3; 54 pruebas aprobadas; nueva auditoría local sin avisos conocidos. | Workflow añadido, todavía pendiente verificar su ejecución remota en esta rama. | CI |
| AM-07 | GitHub / Dokploy / respaldos: divulgación de secretos o datos. | Media / Alto | P1 | Variables de entorno y exclusiones locales observadas. | Pendiente escaneo exhaustivo del historial, revisión de permisos y almacenamiento externo del respaldo temporal. | Operación |
| AM-08 | PostgreSQL: escrituras parciales, duplicados o pérdida de datos. | Media / Alto | P1 | Transacciones y pruebas S12; migraciones aplicadas en servidor. | SQLite no prueba bloqueo concurrente PostgreSQL. Respaldo creado con índice legible, sin restauración ensayada. | Backend / operación |
| AM-09 | Login y rutas públicas: abuso por intentos repetidos. | Media / Alto | P2 | No se acredita limitación de frecuencia ni resistencia a carga abusiva. | Pendiente revisar e implementar controles medidos. | Backend / operación |

## 5. Plan de mitigación

1. Operación: verificar HTTPS antes de utilizar datos o contraseñas reales.
   Activar cookies Secure cuando el acceso HTTPS funcione.
2. Backend: ampliar pruebas de autorización y CSRF a las operaciones restantes.
3. CI: ejecutar y revisar el nuevo workflow de auditoría; conservar artefactos.
4. Operación: extraer el respaldo temporal a almacenamiento protegido y
   ensayar restauración en una base aislada.
5. Equipo: revisar secretos del historial y permisos de infraestructura.
6. Backend: evaluar revocación de enlaces y límites de intentos.
7. Arquitectura: actualizar diagramas y trazabilidad con los controles reales.

Criterio de cierre: cada acción debe tener responsable asignado, evidencia
enlazada y resultado verificable. Las propuestas no se marcan como ejecutadas.

## 6. Privacidad y datos tratados

| Categoría | Finalidad | Acceso previsto / límite |
|---|---|---|
| Nombre y correo de cuenta | Identificar y autenticar al organizador. | Cuenta propia y operación autorizada. |
| Hash de contraseña | Verificar credenciales. | Backend; no mostrar en pantallas, logs ni evidencias. |
| Datos de evento y tareas | Organizar el evento. | Propietario; invitado solo en el alcance expresamente permitido por su enlace. |
| Nombre, correo y asistencia de invitados | Gestionar invitaciones y respuestas. | Propietario y alcance individual autorizado. |
| Tokens y cookies | Autorizar consultas o mantener sesión. | Tratarlos como secretos; evitar copiarlos en evidencias. |
| Logs, métricas y respaldos | Diagnóstico y recuperación. | Acceso operativo restringido; política de retención pendiente. |

Base y alcance de uso:
- La finalidad declarada es una demostración académica con datos ficticios.
- Esto no acredita consentimiento ni una base jurídica para datos personales
  reales. No se autoriza aquí un uso productivo con personas reales.
- El equipo debe comprobar que los datos del entorno público sean ficticios.
- El envío automático de correos sigue siendo un experimento simulado.
- No existe política completa verificada de retención, eliminación y derechos
  de los titulares; queda pendiente antes de utilizar datos reales.
- Cerrar un evento conserva información en Historial; no equivale a eliminarla.
- Los respaldos también pueden contener datos y requieren protección.
- El CSS importa fuentes externas; debe incluirse esa dependencia en la revisión
  de privacidad y considerarse alojamiento local de fuentes.
- No se integra un LLM al producto; la IA se utiliza como apoyo de desarrollo.

## 7. Riesgo residual y decisión del equipo

No se declara aceptado por el equipo ningún riesgo sin revisión expresa.

Se propone limitar la demostración a información ficticia y credenciales
exclusivas de prueba mientras se resuelve HTTPS. Esto reduce el impacto de
exposición, pero no elimina el riesgo de transporte ni sustituye TLS.

La falta de limitación de frecuencia, la revisión incompleta de secretos y
la restauración no ensayada permanecen abiertas.

## 8. Evidencias

- [Auditoría y tratamiento](auditoria-dependencias.md).
- [Pruebas posteriores a actualización](../evidencias/pruebas-pytest-9.txt).
- [Pruebas de métricas](../../tests/test_metrics_auth.py).
- [Consistencia](../../tests/test_consistencia_s12.py).
- [Historial y configuración](../../tests/test_historial_configuracion.py).
- [Riesgos y fallos](../arc42/11-riesgos-y-deuda-técnica.md).
- [Aplicación](../../app/web.py).