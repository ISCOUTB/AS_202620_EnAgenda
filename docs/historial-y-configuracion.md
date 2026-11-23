# Historial y Configuración

## Comportamiento

- Mis eventos muestra eventos activos, con el límite existente de cuatro.
- En el detalle se puede finalizar o cancelar, previa confirmación en el formulario.
- El cierre es manual y definitivo desde la interfaz; conserva fechas, ubicación,
  invitados, enlaces y estados de respuesta. Se consulta desde Historial con filtro.
- Las invitaciones de eventos cerrados muestran el cierre y no aceptan respuestas.
- Configuración permite editar nombre/correo, cambiar contraseña y elegir violeta,
  rosa, verde o azul. El color se aplica a las pantallas privadas de organización;
  la invitación pública mantiene su diseño.
- Perfil y contraseña requieren la contraseña actual. La contraseña nueva debe
  tener 8–128 caracteres y confirmación coincidente. El correo debe ser único.

## Archivos y persistencia

Casos de uso: `src/eventos/aplicacion/cerrar_evento.py` y
`src/usuarios/aplicacion/configurar_cuenta.py`. Rutas: `/historial`,
`/configuracion` y POST `/eventos/<id>/cerrar`. Las rutas requieren sesión activa;
los POST requieren CSRF. Cada consulta de historial está acotada al propietario.

Migración `d91f6a2c804e`, posterior a `b303d9dbf5e5`: añade `usuarios.tema`.
Ejecutar `python -m alembic upgrade head` con la configuración correcta antes
iniciar la aplicación actualizada. Ver instrucciones completas del paquete.

## Validación

50 pruebas aprobadas en Python 3.12, incluyendo la suite previa y los experimentos.
Los nuevos tests prueban permisos, cierre, conservación de respuestas, cupo liberado,
protección CSRF, correo duplicado, contraseña, persistencia de color y migración
sobre datos existentes. SQLite aislado no verifica bloqueos PostgreSQL reales.
Los archivos `__init__.py` agregados a experimentos corrigen la colección de sus
pruebas: el ZIP traía `_init_.py`, que Python no reconoce como inicializador.

No se comprobaron Docker, el despliegue ni la presentación visual en navegador en
el entorno de revisión. Las contraseñas no se devuelven en HTML ni se registran.
