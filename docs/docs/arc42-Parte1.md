 # 1. Introducción

Organizar un evento por pequeño que sea suele convertirse en un dolor de cabeza cuando la información termina dispersa entre chats de WhatsApp, notas de voz, correos y hojas de cálculo improvisadas.

EnAgenda nace para resolver esa fragmentación, reuniendo en una sola plataforma todo lo necesario para planificar y gestionar un evento de principio a fin.

Desde la lista de invitados y sus confirmaciones de asistencia, hasta el cronograma de actividades, las tareas pendientes, la lista de compras y el control del presupuesto; EnAgenda ofrece a los organizadores una vista panorámica, clara y organizada para tomar decisiones rápidas sin que se traspapele ningún detalle.

 ## 1.1 Problema a Resolver

Planear una reunión, una celebración o un evento pequeño exige coordinar múltiples variables en tiempo real. Al no contar con un espacio unificado, la mayoría de los organizadores terminan confiando en su memoria o en herramientas desconectadas entre sí.

Esta falta de centralización genera inconvenientes recurrentes:

- Información desactualizada o perdida entre múltiples canales de conversación.
- Falta de visibilidad sobre los avances, lo que dificulta saber qué tareas o compras siguen pendientes.
- Incertidumbre en la gestión del presupuesto, lo que suele derivar en gastos no planificados.

EnAgenda ataca esta problemática de raíz, ofreciendo una plataforma centralizada que simplifica y estructura toda la logística en un solo lugar.

 ## 1.2 Stakeholders

| Stakeholder | Necesidad e Interés Principal |
|------------|-------------------------------|
| Propietario del evento | Mantener el control total de la logística, los gastos y el avance de los preparativos de forma simple y centralizada. |
| Invitado | Consultar los detalles del evento (fecha, hora, ubicación) y confirmar su asistencia en pocos pasos. |
| Equipo de desarrollo | Diseñar y construir una solución de software sólida, mantenible y escalable a largo plazo. |
| Docente evaluador | Validar la correcta implementación de los principios de arquitectura de software y buenas prácticas de ingeniería. |

 ## 1.3 Objetivos del Sistema

- Unificar la información: Concentrar todos los datos logísticos de un evento en un único punto accesible.
- Agilizar la gestión de asistentes: Simplificar el envío de información y la recepción de confirmaciones de asistencia.
- Dar seguimiento operativo: Facilitar la asignación y control de tareas pendientes y recursos requeridos.
- Transparentar las finanzas: Ofrecer herramientas sencillas para el registro y control del presupuesto y gastos reales.
- Visualizar el estado general: Proporcionar un panorama claro sobre el nivel de preparación del evento antes del día fijado.

 ## 1.4 Objetivos de Calidad

| Prioridad | Objetivo | Criterio de Éxito |
|-----------|----------|-------------------|
| Alta | Usabilidad | Un usuario nuevo debe poder registrarse y crear un evento listo para compartir en menos de 5 minutos, sin requerir asistencia previa. |
| Alta | Rendimiento | Las interacciones principales y tiempos de respuesta de la plataforma no superarán los 2 segundos bajo condiciones normales de tráfico. |
| Alta | Disponibilidad | El servicio mantendrá un tiempo de actividad (uptime) mínimo del 99%, garantizando que la información esté accesible cuando se necesite. |
| Media | Seguridad | Control de acceso riguroso: únicamente el propietario tendrá permisos de edición sobre la administración del evento. |
| Media | Mantenibilidad | Arquitectura limpia y modular que facilite la incorporación de nuevas funcionalidades sin afectar la estabilidad existente. |
