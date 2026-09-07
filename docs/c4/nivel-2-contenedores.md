# C4 - Nivel 2: Contenedores

```mermaid
C4Container
    title Diagrama de Contenedores - EnAgenda

    Person(organizador, "Propietario del evento", "Persona encargada de organizar y administrar el evento")
    Person(invitado, "Invitado", "Persona invitada que consulta la información y confirma su asistencia")

    System_Boundary(enagenda, "EnAgenda") {

        Container(webApp, "Aplicación Flask", "Python / Flask", "Recibe las solicitudes HTTP y presenta las funcionalidades de EnAgenda.")

        Container(invitaciones, "Módulo de Invitaciones", "Python", "Permite crear, consultar y gestionar invitaciones.")

    }

    ContainerDb(repositorio, "Repositorio en memoria", "Python", "Almacena temporalmente las invitaciones durante la ejecución de la aplicación.")

    Rel(organizador, webApp, "Utiliza", "HTTP")
    Rel(invitado, webApp, "Consulta y responde invitaciones", "HTTP")
    Rel(webApp, invitaciones, "Gestiona invitaciones", "Llamada interna")
    Rel(invitaciones, repositorio, "Guarda y consulta invitaciones", "Llamada interna")
```
