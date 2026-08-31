# 12. Glosario

Este glosario define los principales términos funcionales, de negocio y
arquitectónicos utilizados en la documentación de EnAgenda.

| Término | Definición |
|---|---|
| **EnAgenda** | Aplicación web responsive orientada a centralizar y facilitar la planificación y gestión de eventos pequeños. |
| **Evento** | Actividad organizada que contiene información necesaria para su planificación, como invitados, tareas, agenda, elementos necesarios y presupuesto. |
| **Propietario del evento** | Usuario responsable de crear y administrar un evento, incluyendo sus invitados, tareas, agenda, elementos y presupuesto. |
| **Invitado** | Persona que recibe una invitación a un evento y puede consultar la información permitida y gestionar su propia respuesta de asistencia. |
| **Invitación** | Registro que vincula a un invitado con un evento y permite gestionar su participación mediante un enlace individual. |
| **Enlace individual** | Enlace asociado a una invitación específica que permite al invitado acceder a la información autorizada y gestionar su respuesta sin crear una cuenta. |
| **Token** | Identificador utilizado para localizar una invitación mediante su enlace individual. Debe ser no predecible para evitar el acceso no autorizado a otras invitaciones. |
| **Vigencia de la invitación** | Periodo durante el cual una invitación permite al invitado consultar la información autorizada y registrar o modificar su respuesta. |
| **Fecha límite de respuesta** | Fecha y hora a partir de la cual una invitación deja de estar vigente y el invitado ya no puede consultar ni modificar su respuesta. |
| **Estado de invitación** | Estado actual asociado a una invitación. En EnAgenda puede ser `PENDIENTE`, `CONFIRMADO` o `NO_ASISTIRE`. |
| **Pendiente** | Estado que indica que el invitado todavía no ha registrado una decisión sobre su asistencia. |
| **Confirmado** | Estado que indica que el invitado ha confirmado que asistirá al evento. |
| **No asistiré** | Estado que indica que el invitado ha informado que no participará en el evento. |
| **Respuesta de asistencia** | Decisión registrada por el invitado respecto a su participación en el evento. Puede modificarse mientras la invitación permanezca vigente. |
| **Estado vigente** | Último estado válido asociado a una invitación y utilizado para representar su situación actual en el sistema. |
| **Panel de seguimiento** | Espacio destinado al propietario del evento para consultar el estado general de preparación y los resultados de las invitaciones. |
| **Conteo de asistencia** | Cantidad de invitaciones agrupadas según su último estado vigente: `Pendiente`, `Confirmado` o `No asistiré`. |
| **Tarea** | Actividad pendiente relacionada con la organización del evento que puede ser registrada y gestionada por el propietario. |
| **Agenda** | Organización temporal de las actividades planificadas para el evento. |
| **Elemento necesario** | Recurso, objeto o insumo que debe ser considerado dentro de la planificación del evento. |
| **Presupuesto** | Registro destinado a planificar y controlar los recursos económicos asociados al evento. |
| **Gasto real** | Valor efectivamente gastado durante la organización del evento y utilizado para comparar el comportamiento del presupuesto. |
| **Control de acceso** | Mecanismo que determina qué información y operaciones puede realizar un actor según su rol y el alcance de su invitación. |
| **Propietario** | Actor con permisos para administrar los elementos del evento que le pertenece. |
| **Actor** | Persona que interactúa con EnAgenda. En el alcance actual se consideran principalmente el propietario del evento y el invitado. |
| **Monolito modular** | Estilo arquitectónico utilizado por EnAgenda en el que la aplicación se despliega como una única unidad, pero se organiza internamente en módulos funcionales separados. |
| **Módulo** | Unidad funcional de la aplicación que concentra responsabilidades relacionadas con un área específica del dominio. EnAgenda contempla módulos como eventos, invitaciones, tareas, agenda, presupuesto y panel. |
| **Dominio** | Parte de un módulo que contiene las entidades y reglas propias del negocio, independientes de la interfaz web y de los mecanismos de persistencia. |
| **Caso de uso** | Operación de aplicación que coordina una acción concreta del sistema, utilizando las reglas del dominio y los mecanismos de infraestructura necesarios. |
| **Infraestructura** | Parte del sistema responsable de implementar mecanismos técnicos como la persistencia y recuperación de información. |
| **Entidad `Invitacion`** | Objeto del dominio que representa una invitación y contiene su token, destinatario, fecha límite y estado, además de las reglas para comprobar su vigencia y cambiar su estado. |
| **`EstadoInvitacion`** | Enumerado que representa los estados válidos de una invitación: `PENDIENTE`, `CONFIRMADO` y `NO_ASISTIRE`. |
| **`GestionarInvitacion`** | Componente de la capa de aplicación encargado de coordinar las operaciones relacionadas con la gestión de invitaciones. |
| **Repositorio de invitaciones** | Componente encargado de almacenar y recuperar invitaciones mediante su token. |
| **Repositorio en memoria** | Implementación de persistencia utilizada actualmente para almacenar temporalmente las invitaciones durante la ejecución del sistema. |
| **Server Action** | Mecanismo de Next.js utilizado como punto de entrada para procesar determinadas operaciones provenientes de la interfaz web y delegarlas a los módulos correspondientes. |
| **Responsive** | Característica de la aplicación web que permite adaptar su interfaz a diferentes tamaños de pantalla, incluyendo computadores y dispositivos móviles. |
| **HTTPS** | Protocolo utilizado para proteger la comunicación entre los usuarios y la aplicación web. |
| **EC** | Identificador utilizado para los escenarios de calidad de EnAgenda, como EC-01 de aislamiento entre invitaciones y EC-05 de rendimiento de operaciones principales. |
