# C4 - Nivel 3: Componentes

```mermaid
C4Component
    title Diagrama de Componentes - Módulo de Invitaciones

    Person(organizador, "Organizador", "Administra el evento")
    Person(invitado, "Invitado", "Consulta y responde invitaciones")

    Container(webApp, "Aplicación Flask", "Python / Flask", "Recibe solicitudes HTTP y ofrece las funciones de EnAgenda.")

    Container_Boundary(invitaciones, "Módulo de Invitaciones") {
        Component(controlador, "Controlador de Invitaciones", "Python", "Recibe y dirige las solicitudes.")
        Component(servicio, "Servicio de Invitaciones", "Python", "Crea, consulta y gestiona invitaciones.")
        Component(modelo, "Modelo de Invitación", "Python", "Representa los datos de una invitación.")
    }

    ContainerDb(repositorio, "Repositorio en Memoria", "Python", "Almacena temporalmente las invitaciones.")

    Rel(organizador, webApp, "Administra el evento", "HTTP")
    Rel(invitado, webApp, "Consulta y responde", "HTTP")

    Rel(webApp, controlador, "Envía solicitudes", "Llamada interna")
    Rel(controlador, servicio, "Solicita operaciones", "Llamada interna")
    Rel(servicio, modelo, "Utiliza", "Llamada interna")
    Rel(servicio, repositorio, "Guarda y consulta", "Llamada interna")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")

    UpdateRelStyle(organizador, webApp, $textColor="#1d4ed8", $lineColor="#1d4ed8", $offsetY="-30")
    UpdateRelStyle(invitado, webApp, $textColor="#047857", $lineColor="#047857", $offsetY="30")

    UpdateRelStyle(webApp, controlador, $textColor="#7c3aed", $lineColor="#7c3aed", $offsetY="-25")
    UpdateRelStyle(controlador, servicio, $textColor="#7c3aed", $lineColor="#7c3aed", $offsetX="-30")
    UpdateRelStyle(servicio, modelo, $textColor="#7c3aed", $lineColor="#7c3aed", $offsetX="30")
    UpdateRelStyle(servicio, repositorio, $textColor="#b45309", $lineColor="#b45309", $offsetY="30")
```


