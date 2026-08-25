# 0001 — Usar monolito modular

- Estado: Aceptado
- Fecha: 2026-08-23
- Decide: Equipo EnAgenda
- Escenarios de calidad relacionados: EC-01, EC-02, EC-03, EC-04 y EC-05

## Contexto

EnAgenda es una aplicación web responsive para organizar eventos pequeños. El
sistema permitirá crear y editar eventos, gestionar invitados, generar
invitaciones individuales, registrar respuestas de asistencia, administrar
tareas, agenda, presupuesto básico y consultar un panel de seguimiento.

Los invitados accederán sin crear una cuenta mediante enlaces individuales. Cada
enlace tendrá una fecha límite de respuesta independiente de la fecha del evento.
Mientras esté vigente, permitirá consultar la información autorizada y cambiar el
estado entre `Pendiente`, `Confirmado` y `No asistiré`. Después del vencimiento,
el enlace bloqueará el acceso y los cambios.

El sistema será construido por un equipo de tres estudiantes. Debe poder
desarrollarse, probarse y desplegarse con herramientas gratuitas o de capa
gratuita. La arquitectura debe proteger la privacidad de las invitaciones,
mantener consistencia entre las respuestas y los conteos del panel, y permitir
evolucionar el sistema sin introducir complejidad innecesaria.

La aplicación web responsive será el único cliente previsto para el proyecto.
Por esta razón, no se requiere una API pública ni un backend separado.

## Alternativas consideradas

### A. Arquitectura en capas

La arquitectura en capas separa el sistema por responsabilidades técnicas, por
ejemplo presentación, aplicación o negocio y persistencia.

#### A favor

- Es un enfoque conocido y fácil de iniciar.
- Separa responsabilidades técnicas.
- Puede implementarse y desplegarse como una sola aplicación.

#### En contra

- Las reglas de un mismo dominio pueden quedar repartidas entre varias capas.
- No expresa claramente los límites entre eventos, invitaciones, tareas, agenda,
  presupuesto y panel.
- Puede favorecer dependencias amplias hacia una persistencia compartida.

#### Por qué no se eligió

Aunque es viable, se prefiere una estructura cuya organización principal esté
alineada con las áreas del negocio de EnAgenda. La separación por capas se usará
de forma ligera dentro de los módulos, pero no será el criterio principal de
organización del sistema.

### B. Arquitectura hexagonal

La arquitectura hexagonal separa el núcleo de negocio de sus dependencias externas
mediante puertos y adaptadores.

#### A favor

- Facilita aislar las reglas de vigencia, privacidad y actualización de
  invitaciones de frameworks y persistencia.
- Favorece pruebas de reglas de negocio sin depender de infraestructura.
- Puede incorporar una interfaz web, una API o integraciones externas mediante
  adaptadores específicos.

#### En contra

- Introduce puertos, adaptadores e interfaces adicionales desde el inicio.
- Aumenta el número de archivos y abstracciones para el alcance actual.
- Incrementa la curva de aprendizaje y el costo de mantenimiento para el equipo.
- Puede llevar a abstraer tecnologías que todavía no necesitan cambiar.

#### Por qué no se eligió

Los beneficios de una arquitectura hexagonal completa no compensan todavía el
costo de complejidad inicial para el proyecto y el equipo actual. 

### C. Monolito modular

El monolito modular organiza una única aplicación desplegable en módulos de
negocio con responsabilidades, límites y dependencias explícitas.

#### A favor

- Alinea la estructura del código con el dominio de EnAgenda.
- Permite concentrar la vigencia, privacidad y actualización de respuestas en el
  módulo de invitaciones.
- Reduce el costo de despliegue y operación al mantener un solo artefacto.
- Facilita distribuir el trabajo entre los integrantes por módulos de negocio.
- Permite usar una aplicación web full-stack con Server Actions sin crear una API
  pública ni un backend separado.
- Permite mantener los módulos separados y evaluar su evolución de forma
independiente si el proyecto lo requiere.

#### En contra

- Requiere disciplina para evitar dependencias directas entre módulos.
- Los cambios requieren desplegar la aplicación completa.
- Los módulos comparten proceso y recursos.
- Una mala separación puede convertirlo en un monolito acoplado.

## Decisión

Se elige un monolito modular como estilo arquitectónico principal para EnAgenda.

La aplicación se organizará inicialmente en los módulos `eventos`,
`invitaciones`, `tareas`, `agenda`, `presupuesto` y `panel`.

Cada módulo tendrá una estructura interna ligera que separe la lógica de negocio,
los casos de uso de aplicación y el acceso a infraestructura. 

La capa web será el punto de entrada de los usuarios. Las páginas, componentes y
Server Actions de Next.js delegarán los casos de uso a los módulos. Esta capa no
deberá contener reglas de negocio ni acceder directamente a los detalles de
persistencia.

EnAgenda no expondrá una API pública ni utilizará un backend separado, porque la
aplicación web responsive será el único cliente previsto para el proyecto.

Los módulos no accederán directamente a los detalles internos de otros módulos.
Cuando necesiten intercambiar información, utilizarán contratos o servicios
explícitos dentro de la misma aplicación.

## Consecuencias

### Positivas

- El equipo construirá, probará y desplegará una sola aplicación.
- Los módulos reflejarán las áreas funcionales principales del sistema.
- Las reglas de enlaces individuales, vencimiento y cambio de respuesta se
  concentrarán en el módulo de invitaciones.
- La organización interna reduce la mezcla entre interfaz web, reglas de negocio
  y acceso a infraestructura.
- La estructura permite comenzar con una solución simple y evolucionarla según
  evidencia de uso, pruebas y necesidades técnicas reales.

### Negativas y costos asumidos

- El equipo debe mantener disciplina sobre las dependencias entre módulos.
- Los cambios se despliegan junto con toda la aplicación.
- La separación interna por capas debe mantenerse ligera; crear abstracciones sin
  necesidad concreta puede aumentar la complejidad sin aportar valor.
- Una futura extracción de módulo requerirá definir nuevos contratos, mecanismos
  de comunicación y despliegues independientes.
- Los límites de los módulos deberán revisarse cuando se implementen los primeros
  aspectos funcionales.

### Riesgos y disparadores

- Si se detectan importaciones directas frecuentes hacia detalles internos de
  otros módulos, se revisarán los límites y contratos de los módulos afectados.
- Si un módulo necesita escalar, fallar o desplegarse de forma independiente, se
  evaluará su extracción mediante un ADR posterior.
- Si la carpeta `compartido/` empieza a contener lógica de negocio de varios
  módulos, se revisará su contenido para devolver cada responsabilidad al módulo
  correspondiente.

## Trazabilidad

- Introducción y objetivos:
  `docs/arc42/01-introduccion-y-objetivos.md`
- Restricciones:
  `docs/arc42/02-restricciones.md`
- Contexto y alcance:
  `docs/arc42/03-contexto-y-alcance.md`
- Estrategia de solución:
  `docs/arc42/04-estrategia-de-solucion.md`
- Requisitos de calidad y escenarios:
  `docs/arc42/10-requisitos-de-calidad.md`
- Matriz comparativa:
  `docs/arquitectura/matriz-comparativa-estilos.md`
- C4 afectado:
  nivel 2 y nivel 3 pendientes de elaborar en las siguientes entregas
- Implementación:
  esqueleto inicial de módulos en `src/`
- Pruebas:
  prueba automatizada de reglas de invitación en `tests/`
- Evidencia:
  comandos de ejecución y prueba documentados en `README.md`
