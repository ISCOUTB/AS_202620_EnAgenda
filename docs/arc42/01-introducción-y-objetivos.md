# 1. Introducción y objetivos

 ## 1. Introducción

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

| Stakeholder | Rol frente al sistema | Necesidad e interés principal |
|---|---|---|
| Propietario del evento | Usuario principal | Crear y administrar eventos, invitados, tareas, agenda, elementos y presupuesto desde un solo lugar. |
| Invitado | Usuario externo | Consultar la información que le corresponde y confirmar o modificar su asistencia mediante un enlace individual. |
| Equipo de desarrollo | Interesado técnico | Mantener una solución que pueda construirse, probarse, desplegarse y evolucionarse dentro del tiempo y recursos del curso. |
| Docente evaluador | Interesado académico | Verificar la trazabilidad entre requisitos, restricciones, decisiones arquitectónicas, código y evidencia. |

 ## 1.3 Objetivos del Sistema

- Unificar la información: Concentrar todos los datos logísticos de un evento en un único punto accesible.
- Agilizar la gestión de asistentes: Simplificar el envío de información y la recepción de confirmaciones de asistencia.
- Dar seguimiento operativo: Facilitar la asignación y control de tareas pendientes y recursos requeridos.
- Transparentar las finanzas: Ofrecer herramientas sencillas para el registro y control del presupuesto y gastos reales.
- Visualizar el estado general: Proporcionar un panorama claro sobre el nivel de preparación del evento antes del día fijado.

 ## 1.4 Objetivos de calidad

| Prioridad | Atributo | Objetivo de calidad | Criterio inicial de éxito |
|---|---|---|---|
| Alta | Privacidad y seguridad | Un invitado que accede mediante un enlace individual solo puede consultar y modificar la respuesta asociada a su propia invitación. | El 100 % de los intentos de acceder a la información privada de otro invitado desde una invitación válida debe ser rechazado en las pruebas de autorización. |
| Alta | Usabilidad | Un organizador sin experiencia previa debe poder crear un evento, registrar la información mínima y generar una invitación compartible. | Al menos 4 de 5 usuarios de prueba completan el flujo en un máximo de 5 minutos, sin ayuda del equipo. |
| Alta | Consistencia | Cada invitado debe tener una única respuesta vigente de asistencia y el panel del organizador debe reflejar correctamente los conteos. | En las pruebas de creación y actualización de respuestas no se generan registros duplicados y los conteos coinciden con los datos almacenados. |
| Media | Rendimiento | Las operaciones principales —consultar una invitación, confirmar asistencia y ver el panel— deben responder con rapidez bajo una carga inicial definida. | El percentil 95 de las respuestas debe ser menor a 2 segundos con una carga de prueba que el equipo documentará antes de implementar. |
| Media | Modificabilidad | El sistema debe permitir incorporar nuevas capacidades relacionadas con eventos sin modificar indiscriminadamente todo el código. | Las reglas de negocio de invitados, tareas y presupuesto se organizarán en módulos o componentes separados, verificables mediante la estructura del repositorio y pruebas. |
