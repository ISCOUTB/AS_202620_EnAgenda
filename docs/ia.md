# Registro de Uso de Inteligencia Artificial

## Reglas del equipo

- Todo código generado debe ser revisado.
- Todo código aceptado debe ejecutarse y probarse.
- Las decisiones arquitectónicas pertenecen al equipo.
- No se introducirán datos personales ni credenciales en herramientas externas.
- Se registrarán las propuestas importantes aceptadas, modificadas o rechazadas.

| Fecha | Herramienta | Propósito | Qué se aceptó | Qué se rechazó | Cómo se verificó |
|---|---|---|---|---|---|
| 07-Ago-2026 | Perplexity | Organización inicial del proyecto | Propuesta de estructura para el proyecto | Que existiese un usuario adicional en el proyecto, con el rol de colaborador, el cual se suponía que iba a ser invitado mediante un enlace por el creador/administrador del evento | Por una revisión del equipo, en la cual se consideró el rol de colaborador como innecesario debido a que es un usuario extra que no representa un cambio significativo en el desarrollo del evento, esto sumado al hecho de que la app está pensada para ser intuitiva y que el usuario pueda gestionar sus eventos de manera independiente y sencilla, sin necesidad de terceros para la planeación  |

| Fecha | Herramienta | Propósito | Propuesta o resultado | Qué se aceptó | Qué se rechazó o modificó | Cómo se verificó |
|---|---|---|---|---|---|---|
| 08-Ago-2026 | Perplexity | Definir el mecanismo de invitaciones | Se propuso enviar invitaciones mediante correo electrónico | Se aceptó la necesidad de identificar individualmente a cada invitado | Se rechazó el envío obligatorio por correo debido a la exposición potencial de datos personales en un repositorio público, la necesidad de crear correos ficticios para las pruebas y la posibilidad de que los invitados no revisen o no utilicen el correo electrónico | Revisión de la guía del curso, análisis del carácter público del repositorio y discusión del equipo |
| 08-Ago-2026 | Perplexity | Definir una alternativa al envío por correo | Se propuso generar un enlace individual para cada invitado y compartirlo por un medio externo | Se aceptó el uso de enlaces únicos asociados a cada invitación | Se descartó que todos los invitados utilizaran un único enlace común, porque no permitiría identificar correctamente quién respondió | Análisis del flujo de invitaciones y definición de pruebas para tokens válidos, inválidos y repetidos | 

| Fecha | Herramienta | Propósito | Qué se aceptó | Qué se rechazó | Cómo se verificó |
|---|---|---|---|---|---|
| 15-Ago-2026 | Mermaid | Asistencia en la elaboración del diagrama C4 Context de EnAgenda, utilizando principalmente las guías y documentación proporcionadas por Mermaid. | La estructura y sintaxis recomendada por Mermaid para representar el sistema EnAgenda. | Elementos que no eran necesarios para el C4 Context, como System_Boundary, bases de datos, colas y otros componentes que no correspondían al nivel 1 de un C4. | Se verificó el código mediante el renderizado del diagrama en Mermaid y se comprobó que la estructura correspondiera a un diagrama C4 Context. |


| Fecha | Herramienta | Propósito | Qué se aceptó | Qué se rechazó | Cómo se verificó |
|---|---|---|---|---|---|
| 29/08/2026 | ChatGPT | Revisar el estado del repositorio, organizar Git y Visual Studio Code y definir la estructura del código fuente. | Se aceptó separar la documentación en `docs/` y el código en `src/`, además de organizar el módulo de Invitaciones en `aplicacion/`, `dominio/` e `infraestructura/`. | Se rechazaron estructuras más complejas o distribuidas que no eran necesarias para el alcance de la Semana 4. | Se verificó la estructura mediante comandos de PowerShell y Git, incluyendo `git status` y la inspección de directorios. |
| 29/08/2026 | ChatGPT | Limpiar el repositorio y configurar los archivos necesarios para evitar contenido generado localmente. | Se aceptó eliminar archivos basura y configurar `.gitignore` para excluir archivos generados durante el desarrollo. | Se rechazaron archivos temporales y generados localmente que no debían formar parte del repositorio. | Se verificó mediante `git status` y comandos de comprobación de archivos ignorados. |
| 30/08/2026 | ChatGPT | Implementar el módulo de Invitaciones y hacer funcional la estructura de `src/`. | Se aceptó separar Invitaciones en aplicación, dominio e infraestructura, implementando `GestionarInvitacion`, `Invitacion`, `EstadoInvitacion` y `RepositorioInvitacionesMemoria`. | Se rechazó incorporar una base de datos real en esta etapa y se mantuvo el repositorio en memoria. | Se ejecutó `pytest -q` y se obtuvieron `6 passed`. También se revisaron las rutas y archivos mediante PowerShell. |
| 30/08/2026 | ChatGPT | Crear la interfaz web mínima y conectar el código mediante un primer corte vertical. | Se aceptó utilizar Flask en `app/web.py` como punto de entrada y conectarlo con `GestionarInvitacion`, siguiendo el flujo `Flask → aplicación → dominio → repositorio`. | Se descartó la propuesta anterior basada en Next.js y Server Actions. Tampoco se creó un backend separado ni una API pública. | Se ejecutó `python -u app\web.py` desde la raíz y Flask inició correctamente en `http://127.0.0.1:5000`. |
| 30/08/2026 | ChatGPT | Revisar y alinear la arquitectura documentada con la implementación real del repositorio. | Se aceptó actualizar arc42, el ADR y C4 nivel 2 para reflejar Flask, `src/invitaciones/` y el repositorio en memoria. | Se rechazó documentar como implementados componentes que todavía no existen, como una base de datos, otros servicios independientes o C4 nivel 3. | Se comparó la documentación con la estructura real del repositorio, las pruebas ejecutadas y el arranque de la aplicación. |
