# 8. Conceptos Transversales

Los conceptos transversales de EnAgenda representan reglas y mecanismos
que afectan a diferentes módulos de la aplicación y que deben mantenerse
de forma consistente durante su implementación.

## 8.1 Control de acceso y privacidad

EnAgenda diferencia principalmente dos tipos de actores:

- Propietario del evento.
- Invitado.

El propietario puede administrar los eventos que le corresponden y sus
elementos asociados, incluyendo invitados, tareas, agenda, elementos
necesarios, presupuesto y panel de seguimiento.

El invitado no requiere una cuenta. Su acceso se realiza mediante un
enlace individual asociado a una invitación.

Cada operación realizada mediante una invitación debe comprobar:

1. Que el identificador de la invitación sea válido.
2. Que la invitación exista.
3. Que la invitación se encuentre vigente.
4. Que la operación corresponda al alcance permitido para dicha
   invitación.

El invitado únicamente puede consultar la información permitida y
modificar su propia respuesta de asistencia.

## 8.2 Vigencia de las invitaciones

Las invitaciones tienen una fecha y hora límite de respuesta
independiente de la fecha y hora del evento.

La vigencia debe comprobarse antes de permitir operaciones sobre una
invitación.

Mientras la invitación se encuentre vigente, el invitado puede registrar
o modificar su respuesta.

Una vez superada la fecha límite, el sistema debe rechazar las
operaciones correspondientes.

Esta regla se concentra principalmente en el dominio de Invitaciones y
debe ser respetada por los puntos de entrada que permitan acceder o
modificar una invitación.

## 8.3 Estados y consistencia

Las invitaciones utilizan un conjunto limitado de estados:

- `PENDIENTE`
- `CONFIRMADO`
- `NO_ASISTIRE`

Cada invitación debe conservar un único estado vigente.

Cuando el invitado cambia su respuesta, el nuevo estado reemplaza al
estado anterior como representación actual de su asistencia.

Los conteos mostrados en el panel deben calcularse utilizando el último
estado vigente de cada invitación y no deben considerar respuestas
duplicadas.

## 8.4 Validación de datos

Las operaciones del sistema deben validar los datos antes de modificar
el estado de las entidades.

En el módulo de Invitaciones se validan, entre otros aspectos:

- existencia de la invitación;
- vigencia de la invitación;
- pertenencia del estado recibido al conjunto de estados válidos.

Las reglas propias del negocio deben permanecer en la capa de dominio y
no depender directamente de la interfaz web.

## 8.5 Manejo de errores

Las operaciones que no pueden completarse deben producir errores
controlados que permitan identificar la causa del rechazo.

Entre las situaciones contempladas para Invitaciones se encuentran:

- invitación inexistente;
- invitación vencida;
- estado de invitación no válido;
- intento de operación fuera del alcance permitido.

La capa de aplicación coordina el caso de uso y el dominio determina si
las reglas correspondientes permiten realizar la operación.

## 8.6 Separación de responsabilidades

EnAgenda utiliza una organización interna basada en módulos y una
separación ligera entre:

- aplicación;
- dominio;
- infraestructura.

La capa de aplicación coordina los casos de uso.

La capa de dominio contiene las entidades y reglas de negocio.

La infraestructura implementa los mecanismos técnicos necesarios para
almacenar y recuperar información.

La interfaz web no debe contener directamente las reglas de negocio ni
acceder a los detalles internos de persistencia.

## 8.7 Comunicación con la interfaz web

La aplicación web constituye el punto de entrada de las operaciones
realizadas por los usuarios.

Las Server Actions reciben determinadas operaciones provenientes de los
formularios de la interfaz y las delegan a los módulos correspondientes.

Las reglas de negocio permanecen fuera de la interfaz y son ejecutadas
por las capas correspondientes de cada módulo.

No se contempla una API pública independiente para el alcance actual
del proyecto.

## 8.8 Persistencia

La persistencia se mantiene separada de las reglas de negocio mediante
repositorios.

En el módulo de Invitaciones existe actualmente una implementación
denominada `RepositorioInvitacionesMemoria`, encargada de almacenar y
recuperar invitaciones mediante su token.

Esta separación permite reemplazar posteriormente el mecanismo de
persistencia sin modificar directamente las reglas principales del
dominio.

## 8.9 Configuración y protección de secretos

La configuración sensible del sistema no debe almacenarse directamente
en el repositorio público.

Los datos de configuración que puedan contener información sensible
deben manejarse mediante variables de entorno o mecanismos equivalentes.

No se utilizarán credenciales, secretos ni datos personales reales en
el repositorio ni en las demostraciones del proyecto.

## 8.10 Diseño responsive

EnAgenda se desarrolla como una aplicación web responsive.

La interfaz debe adaptarse a diferentes tamaños de pantalla para permitir
su utilización desde computadores y dispositivos móviles.

Este concepto afecta principalmente a la capa de presentación y debe
mantenerse al desarrollar las diferentes funcionalidades del sistema.

## 8.11 Trazabilidad de los conceptos transversales

Los conceptos anteriores se relacionan directamente con los requisitos de
calidad y restricciones definidos para EnAgenda:

| Concepto transversal | Relación |
|---|---|
| Control de acceso | R-06, EC-01 |
| Vigencia de invitaciones | R-03, EC-02 |
| Estados y consistencia | EC-03, EC-04 |
| Validación y errores | EC-01, EC-02, EC-03 |
| Separación de responsabilidades | ADR-0001 |
| Persistencia | Estrategia de solución y vista de bloques |
| Protección de secretos | R-04 |
| Diseño responsive | R-02 |
| Rendimiento | EC-05 |

Los conceptos transversales deben aplicarse de manera consistente en los
módulos que formen parte de la implementación del MVP.
