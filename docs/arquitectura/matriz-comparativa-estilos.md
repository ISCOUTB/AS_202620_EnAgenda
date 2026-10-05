# Matriz comparativa de estilos arquitectónicos

## Contexto

EnAgenda es una aplicación web responsive orientada a la organización de eventos pequeños. El sistema contempla la creación y administración de eventos, invitados, invitaciones individuales, respuestas de asistencia, tareas, agenda, presupuesto básico y un panel de seguimiento.

Los invitados acceden mediante un enlace individual, sin necesidad de crear una cuenta. Cada invitación cuenta con una fecha límite independiente de la fecha del evento. Mientras la invitación se encuentre vigente, el invitado puede registrar o actualizar su respuesta entre `Pendiente`, `Confirmado` y `No asistiré`. Después del vencimiento, las operaciones sobre la invitación quedan restringidas de acuerdo con las reglas definidas por el dominio.

El equipo está compuesto por tres estudiantes. La solución debe poder construirse, probarse y desplegarse manteniendo una complejidad operativa reducida, privacidad en las invitaciones, consistencia en las respuestas y una estructura que pueda evolucionar durante el proyecto.

| Criterio | Arquitectura en capas | Arquitectura hexagonal | Monolito modular |
|---|---|---|---|
| Organización principal | Separa el sistema por responsabilidades técnicas, por ejemplo presentación, aplicación y persistencia | Separa el núcleo de negocio de la infraestructura mediante puertos y adaptadores | Separa la aplicación por módulos de negocio dentro de un único despliegue |
| Ajuste al dominio de EnAgenda | Medio. Las reglas de eventos e invitaciones pueden quedar repartidas entre capas técnicas | Alto. Permite aislar reglas de negocio y adaptadores externos | Alto. Los módulos representan directamente eventos, invitaciones, tareas, agenda, presupuesto y panel |
| Privacidad de enlaces individuales | Puede implementarse en la lógica de negocio, pero exige disciplina para no repartir la validación entre capas | Facilita probar la validación de tokens y vencimiento sin depender de infraestructura | Permite concentrar las reglas de acceso, vigencia y actualización dentro del módulo de invitaciones |
| Consistencia de respuestas y panel | Requiere coordinar las capas para actualizar estados y conteos | Los casos de uso pueden centralizar reglas y puertos de persistencia | Mantiene la actualización de respuestas y los conteos dentro de una sola aplicación y una misma unidad de despliegue |
| Comunicación entre interfaz y servidor | Puede utilizar formularios o endpoints HTTP según la tecnología seleccionada | Usualmente define puertos de entrada y adaptadores web o API | Puede utilizar una capa de entrada web que delegue las operaciones en los casos de uso de los módulos sin requerir servicios independientes |
| Complejidad inicial | Baja a media | Media a alta, por puertos, adaptadores e interfaces adicionales | Media. Requiere definir y respetar módulos, pero evita procesos distribuidos |
| Equipo de tres integrantes | Viable, pero puede dividirse por capas técnicas y generar dependencias frecuentes | Viable, pero implica una curva de aprendizaje y más estructura inicial | Adecuado. Permite repartir trabajo por módulos de negocio y mantener una coordinación simple |
| Despliegue y costo | Puede desplegarse como una sola aplicación | Puede desplegarse como una sola aplicación, con mayor complejidad interna | Un solo artefacto desplegable y menor complejidad operativa |
| Pruebas | Las pruebas pueden depender de capas concretas si no se controlan las dependencias | Favorece pruebas aisladas del dominio | Permite pruebas por módulo mediante una separación ligera de negocio, aplicación e infraestructura |
| Evolución futura | Puede evolucionar, pero las áreas del negocio no quedan delimitadas explícitamente | Facilita reemplazar adaptadores, aunque puede sobredimensionar el proyecto | Permite extraer un módulo posteriormente si existe una razón real de carga, despliegue, disponibilidad o evolución independiente |
| Riesgo principal | Convertirse en capas genéricas que mezclen reglas de dominios diferentes | Sobrearquitectura: abstracciones que no resuelven una necesidad actual | Acoplamiento entre módulos si no se respetan límites y contratos |
| Decisión | No seleccionada como estilo principal | No seleccionada como estilo principal | Seleccionada como estilo principal |

## Conclusión

Se selecciona el **monolito modular** como estilo arquitectónico principal para EnAgenda. Este estilo ofrece el mejor equilibrio entre la separación de las áreas del dominio, la capacidad de un equipo de tres estudiantes, una complejidad operativa reducida y la evolución esperada del proyecto.

Dentro de cada módulo se aplica una separación ligera entre lógica de negocio, casos de uso de aplicación y acceso a infraestructura. Esta organización busca mantener claras las responsabilidades de cada parte del sistema sin agregar una complejidad innecesaria para el alcance actual del proyecto.

EnAgenda se implementa como una aplicación web responsive y se despliega como una única unidad. La entrada web está desarrollada con Flask y se encuentra principalmente en `app/web.py`.

Las solicitudes provenientes de la interfaz web son recibidas por Flask y delegadas a los casos de uso correspondientes. En el módulo de Invitaciones, el flujo implementado actualmente es:

```text
app/web.py
    ↓
GestionarInvitacion
    ↓
Invitacion / EstadoInvitacion
    ↓
RepositorioInvitacionesMemoria
```

La presentación utiliza plantillas Jinja2, HTML y CSS. Las plantillas se encuentran en `app/templates/` y sus estilos en `app/static/css/`.

La aplicación también puede exponer endpoints HTTP dentro de la misma aplicación Flask. Estos endpoints no representan servicios independientes y, por lo tanto, no modifican la decisión de mantener un monolito modular.

La capa de entrada web no debe concentrar las reglas principales del negocio ni los detalles internos de persistencia. Estas responsabilidades permanecen separadas dentro de los módulos correspondientes.

Next.js y Server Actions fueron considerados durante etapas anteriores como posibles mecanismos para implementar la entrada web, pero no forman parte de la implementación actual. La solución vigente utiliza Flask como punto de entrada web.