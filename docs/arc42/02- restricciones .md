# 2. Restricciones

## R-01. Alcance y capacidad del equipo

El MVP será construido por un equipo de tres estudiantes durante el curso.

**Impacto arquitectónico:** se prioriza una solución sencilla y un alcance limitado:
eventos, invitados, enlaces individuales, respuestas de asistencia, tareas, agenda,
elementos necesarios, presupuesto básico y panel de seguimiento. Quedan fuera del
MVP pagos, chat, integraciones externas y notificaciones push.

## R-02. Aplicación web responsive

EnAgenda se implementará como una aplicación web responsive, accesible desde
navegadores de computador y dispositivos móviles.

**Impacto arquitectónico:** organizadores e invitados accederán mediante HTTPS sin
instalar una aplicación. Se evita desarrollar, distribuir y mantener aplicaciones
nativas separadas.

## R-03. Invitaciones sin cuenta y con vencimiento

El invitado podrá consultar su invitación y registrar o modificar su respuesta sin
crear una cuenta. Cada evento tendrá una fecha y hora límite de respuesta,
independiente de la fecha y hora del evento.

Después de la fecha límite, el enlace individual no permitirá consultar ni modificar
la invitación.

**Impacto arquitectónico:** cada invitación requerirá un identificador no predecible
y el sistema deberá validar en cada acceso su vigencia, la fecha límite y el alcance
de la invitación antes de mostrar información o aceptar cambios.

## R-04. Privacidad y repositorio público

No se utilizarán datos personales reales, credenciales ni secretos en el repositorio
público ni en las demostraciones.

**Impacto arquitectónico:** se emplearán datos ficticios, variables de entorno para
configuración sensible y archivos de secretos excluidos del control de versiones.

## R-05. Costo y despliegue

El sistema debe desarrollarse y desplegarse con herramientas gratuitas o de capa
gratuita, sin exigir cuentas personales de pago.

**Impacto arquitectónico:** las opciones de alojamiento, base de datos y
automatización se evaluarán por costo, límites de la capa gratuita, facilidad de
despliegue y posibilidad de reemplazo.

## R-06. Roles y permisos

Solo el propietario del evento podrá administrar sus eventos, invitados, tareas,
agenda, elementos y presupuesto. El invitado solo podrá usar su enlace individual
antes de su vencimiento para consultar la información permitida y gestionar su
propia asistencia.

**Impacto arquitectónico:** las operaciones deberán validar el tipo de actor y el
alcance de la invitación antes de autorizar lecturas o cambios.
