# Tareas, Agenda, Presupuesto y temas

## Temas

Azul clásico es el predeterminado. Las alternativas son Terracota y arena,
Vino y marfil, y Verde y dorado, basadas en las referencias visuales del equipo.
Se conserva la tipografía y estructura del diseño recibido. La configuración
ahora cambia toda la paleta: barra lateral, resúmenes, botones, textos y formularios.
En un navegador sin preferencia, login y registro usan azul. Tras elegir un tema,
el navegador lo recuerda al cerrar sesión. La cuenta conserva su preferencia en
la base; los otros usuarios tienen sus propios temas. Se requiere guardar y recargar
la página; otras pestañas abiertas no se actualizan automáticamente.

## Tareas

Se conserva el modelo, la migración y los casos de uso existentes. Crear, editar,
marcar pendiente/completada y eliminar funcionan por evento. Ahora se aplica el tema
de la cuenta y los eventos cerrados quedan de solo consulta, con bloqueo del lado
servidor aunque se envíe un formulario manual.

## Agenda

CRUD de actividades con título, descripción y responsable opcionales, inicio y fin.
La pantalla muestra orden cronológico y las fechas locales de Cartagena. Se
rechazan actividades superpuestas en el mismo evento. Se permiten actividades
contiguas, actividades de varios días y eventos con varias fechas de agenda.
No hay recordatorios automáticos ni calendario de un proveedor externo.

## Presupuesto

Límite editable por evento (opcional hasta que se defina), lista de gastos con
categoría libre y notas, estado pagado/pendiente, edición y eliminación. Valores
en COP con dos decimales, máximo por valor 9.999.999.999,99. Los formularios aceptan
números sin separadores de miles. Se usa Decimal/Numeric para evitar errores float.

Totales: registrado = suma de todos los gastos; pagado = suma de los marcados;
pendiente = registrado - pagado; disponible = límite - registrado. Si supera el
límite, aparece advertencia. Es registro administrativo, no cobro ni pago bancario.

## Persistencia y acceso

Nuevas tablas: actividades_agenda, presupuestos y gastos. Las vistas requieren
sesión, sus POST usan CSRF y los casos de uso comprueban propiedad y cuenta activa.
Los identificadores de actividad/gasto se comprueban también contra el evento.
El cierre mantiene todos los datos consultables en Historial y bloquea escrituras.
La nueva migración continúa el merge del ZIP recibido; no se modificaron migraciones
ya aplicadas. Downgrade elimina solo las tablas nuevas; por eso no se debe usar como
mecanismo de reparación después de registrar datos nuevos sin respaldarlos.

## Verificación

83 pruebas pasan en Python 3.12: suite existente, CRUD, permisos, CSRF, cierre,
montos inválidos, exactitud decimal, superposiciones, paletas completas y migración
con tareas e invitaciones previas. Se generó SQL PostgreSQL offline sin errores.
Faltan ejecución local Docker/PostgreSQL, concurrencia real y revisión visual final.
