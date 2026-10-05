# 9. Decisiones de Arquitectura

Las principales decisiones de arquitectura de EnAgenda se documentan mediante Architecture Decision Records (ADR). Estos registros contienen el contexto, las alternativas consideradas, la decisión adoptada y sus consecuencias.

## ADR-0001 — Usar monolito modular

Se adopta un **monolito modular** como estilo arquitectónico principal para EnAgenda.

La aplicación se organiza en módulos de negocio como `eventos`, `invitaciones`, `tareas`, `agenda`, `presupuesto` y `panel`, manteniendo una separación interna entre la lógica de negocio, los casos de uso de aplicación y la infraestructura.

La aplicación web actúa como punto de entrada al sistema y está implementada con Flask. Las rutas definidas en `app/web.py` reciben las solicitudes HTTP y delegan las operaciones correspondientes en los casos de uso de los módulos.

En el módulo de Invitaciones, el flujo principal implementado es:

```text
app/web.py
    ↓
GestionarInvitacion
    ↓
Invitacion / EstadoInvitacion
    ↓
RepositorioInvitacionesMemoria