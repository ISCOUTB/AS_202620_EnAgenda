# 7. Vista de Despliegue

## 7.1 Descripción general

EnAgenda se plantea como una aplicación web responsive que puede ser
utilizada desde navegadores de computador y dispositivos móviles.

De acuerdo con la estrategia arquitectónica seleccionada, el sistema se
despliega como una única aplicación basada en un monolito modular. Los
módulos funcionales de EnAgenda se mantienen separados lógicamente dentro
de la aplicación, pero no requieren despliegues independientes.

El acceso de los usuarios se realiza mediante HTTPS.

## 7.2 Elementos del despliegue

El despliegue conceptual de EnAgenda contempla los siguientes elementos:

- **Cliente web:** navegador utilizado por el propietario del evento o
  por el invitado para acceder al sistema.
- **Aplicación EnAgenda:** única unidad desplegable que contiene la
  interfaz web, las Server Actions, los casos de uso y los módulos de
  negocio.
- **Persistencia:** mecanismo utilizado para almacenar y recuperar la
  información necesaria para el funcionamiento del sistema.

## 7.3 Distribución de la aplicación

La aplicación EnAgenda se organiza internamente en los siguientes
módulos:

- Eventos.
- Invitaciones.
- Tareas.
- Agenda.
- Presupuesto.
- Panel.

Estos módulos forman parte de la misma aplicación y no corresponden a
servicios independientes.

La separación modular permite mantener responsabilidades diferenciadas
y facilitar la evolución del sistema sin introducir la complejidad de
múltiples aplicaciones desplegadas por separado.

## 7.4 Acceso del propietario

El propietario del evento accede a EnAgenda mediante un navegador web.

El flujo conceptual es:

```text
Propietario
     |
     | HTTPS
     v
Navegador web
     |
     v
Aplicación EnAgenda
     |
     v
Módulos de negocio
     |
     v
Persistencia
