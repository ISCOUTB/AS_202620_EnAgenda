# C4 - Nivel 1: Contexto

```mermaid
C4Context

    title Diagrama de contexto del sistema EnAgenda

    Person(Organizador, "Organizador", "Propietario del evento")
    Person(Invitado, "Invitado", "Persona invitada que consulta la información y confirma su asistencia")

    System(EnAgenda, "EnAgenda", "Gestiona la información del evento y las confirmaciones de asistencia")

    Rel(Organizador, EnAgenda, "Crea y administra el evento")
    Rel(EnAgenda, Organizador, "Proporciona información e invitaciones")

    Rel(Invitado, EnAgenda, "Consulta información y confirma asistencia")
    Rel(EnAgenda, Invitado, "Proporciona información e invitación")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
    UpdateRelStyle(Organizador, EnAgenda, $offsetY="-20")
    UpdateRelStyle(EnAgenda, Organizador, $offsetY="20")
    UpdateRelStyle(Invitado, EnAgenda, $offsetY="-20")
    UpdateRelStyle(EnAgenda, Invitado, $offsetY="20")
```
# Contexto y alcance

## Contexto de negocio

EnAgenda permite a un organizador centralizar la información operativa de un
evento pequeño. El organizador administra el evento, los invitados, las tareas,
la agenda, los elementos requeridos y un presupuesto básico.

Los invitados acceden mediante un enlace individual. No requieren crear una
cuenta para consultar la información permitida del evento y registrar o
actualizar su respuesta de asistencia.

## Alcance inicial

El MVP incluye:

- Creación y edición de eventos.
- Registro de invitados.
- Generación de enlaces individuales de invitación.
- Consulta y actualización de respuestas de asistencia.
- Gestión básica de tareas.
- Registro de elementos necesarios.
- Agenda básica.
- Presupuesto básico.
- Panel de seguimiento.

El MVP no incluye inicialmente pagos, chat entre participantes, sincronización
con calendarios externos, notificaciones push, integración con redes sociales ni
manejo de datos reales de terceros.

## Interfaces externas

En esta etapa no se han definido sistemas externos obligatorios. La interacción
externa del MVP ocurre directamente entre los usuarios y EnAgenda mediante una
interfaz web protegida con HTTPS.
