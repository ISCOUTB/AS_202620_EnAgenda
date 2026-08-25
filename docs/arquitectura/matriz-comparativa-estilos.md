# Matriz comparativa de estilos arquitectónicos

## Contexto

EnAgenda será una aplicación web responsive para organizar eventos pequeños. El
sistema permitirá crear y administrar eventos, invitados, invitaciones
individuales, respuestas de asistencia, tareas, agenda, presupuesto básico y un
panel de seguimiento.

Los invitados accederán mediante un enlace individual, sin crear una cuenta. Cada
invitación tendrá una fecha límite independiente de la fecha del evento. Mientras
el enlace esté vigente, el invitado podrá cambiar su estado entre `Pendiente`,
`Confirmado` y `No asistiré`. Después del vencimiento, el enlace no permitirá
consultar ni modificar la invitación.

El equipo está compuesto por tres estudiantes. La solución debe poder construirse,
probarse y desplegarse con herramientas gratuitas o de capa gratuita, manteniendo
privacidad en las invitaciones, consistencia en las respuestas y una estructura
que pueda evolucionar durante el proyecto.

| Criterio | Arquitectura en capas | Arquitectura hexagonal | Monolito modular |
|---|---|---|---|
| Organización principal | Separa el sistema por responsabilidades técnicas, por ejemplo presentación, aplicación y persistencia | Separa el núcleo de negocio de la infraestructura mediante puertos y adaptadores | Separa la aplicación por módulos de negocio dentro de un único despliegue |
| Ajuste al dominio de EnAgenda | Medio. Las reglas de eventos e invitaciones pueden quedar repartidas entre capas técnicas | Alto. Permite aislar reglas de negocio y adaptadores externos | Alto. Los módulos representan directamente eventos, invitaciones, tareas, agenda, presupuesto y panel |
| Privacidad de enlaces individuales | Puede implementarse en la lógica de negocio, pero exige disciplina para no repartir la validación entre capas | Facilita probar la validación de tokens y vencimiento sin depender de infraestructura | Permite concentrar las reglas de acceso, vigencia y actualización dentro del módulo de invitaciones |
| Consistencia de respuestas y panel | Requiere coordinar las capas para actualizar estados y conteos | Los casos de uso pueden centralizar reglas y puertos de persistencia | Mantiene la actualización de respuestas y los conteos dentro de una sola aplicación y una misma unidad de despliegue |
| Comunicación entre interfaz y servidor | Puede usar formularios, Server Actions o API según el framework elegido | Usualmente define puertos de entrada y adaptadores web o API | La aplicación web puede usar Server Actions como entrada interna sin exponer una API pública |
| Complejidad inicial | Baja a media | Media a alta, por puertos, adaptadores e interfaces adicionales | Media. Requiere definir y respetar módulos, pero evita procesos distribuidos |
| Equipo de tres integrantes | Viable, pero puede dividirse por capas técnicas y generar dependencias frecuentes | Viable, pero implica una curva de aprendizaje y más estructura inicial | Adecuado. Permite repartir trabajo por módulos de negocio y mantener coordinación simple |
| Despliegue y costo | Puede desplegarse como una sola aplicación | Puede desplegarse como una sola aplicación, con mayor complejidad interna | Un solo artefacto desplegable; menor costo operativo y adecuado para capa gratuita |
| Pruebas | Las pruebas pueden depender de capas concretas si no se controlan las dependencias | Favorece pruebas aisladas del dominio | Permite pruebas por módulo; se aplicará una separación ligera de negocio, aplicación e infraestructura |
| Evolución futura | Puede evolucionar, pero las áreas del negocio no quedan delimitadas explícitamente | Facilita reemplazar adaptadores, aunque puede sobredimensionar el proyecto | Permite extraer un módulo posteriormente si existe una razón real de carga, despliegue, disponibilidad o evolución independiente |
| Riesgo principal | Convertirse en capas genéricas que mezclen reglas de dominios diferentes | Sobrearquitectura: abstracciones que no resuelven una necesidad actual | Acoplamiento entre módulos si no se respetan límites y contratos |
| Decisión | No seleccionada como estilo principal | No seleccionada como estilo principal | Seleccionada como estilo principal |

## Conclusión

Se selecciona el monolito modular como estilo arquitectónico principal para
EnAgenda. Este estilo ofrece el mejor equilibrio entre la separación de las áreas
del dominio, la capacidad de un equipo de tres estudiantes, el bajo costo de
despliegue y la evolución esperada del proyecto.

Dentro de cada módulo se aplicará una separación ligera entre lógica de negocio,
casos de uso y acceso a infraestructura. Esta organización busca mantener claras
las responsabilidades de cada parte del sistema sin agregar una complejidad
innecesaria para el alcance del proyecto.

EnAgenda se desarrollará como una aplicación web responsive. La aplicación web
será el único cliente previsto y utilizará Server Actions para procesar
operaciones iniciadas desde formularios. La entrada web delegará las operaciones
a los módulos correspondientes y no contendrá directamente las reglas de negocio
ni los detalles de persistencia.
