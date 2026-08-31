# 9. Decisiones de Arquitectura

Las principales decisiones de arquitectura de EnAgenda se documentan
mediante Architecture Decision Records (ADR). Estos registros contienen
el contexto, las alternativas consideradas, la decisión adoptada y sus
consecuencias.

## ADR-0001 — Usar monolito modular

Se adopta un **monolito modular** como estilo arquitectónico principal
para EnAgenda.

La aplicación se organiza en módulos de negocio como `eventos`,
`invitaciones`, `tareas`, `agenda`, `presupuesto` y `panel`, manteniendo
una separación interna entre la lógica de negocio, los casos de uso y
la infraestructura.

La aplicación web es el punto de entrada y utiliza Server Actions para
delegar las operaciones a los módulos. No se contempla una API pública
ni un backend separado para el alcance actual del proyecto.

**ADR:** [0001 — Usar monolito modular](../adr/0001-usar-monolito-modular.md)

**Estado:** Aceptado

**Escenarios de calidad relacionados:** EC-01, EC-02, EC-03, EC-04 y EC-05.
