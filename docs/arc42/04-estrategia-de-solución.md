# 4. Estrategia de solución

## 4.1 Enfoque general

EnAgenda se desarrolla como una aplicación web responsive. Los organizadores y los invitados acceden mediante un navegador web. En el entorno desplegado, el acceso se realiza mediante HTTP/HTTPS según la configuración disponible en Dokploy.

Los invitados utilizan enlaces individuales generados mediante tokens únicos para consultar su invitación y registrar o actualizar su respuesta de asistencia antes de la fecha límite establecida.

La solución se construye como una única aplicación desplegable. Este enfoque reduce la complejidad operativa y permite que el equipo desarrolle, pruebe y despliegue el sistema sin necesidad de administrar múltiples servicios independientes.

Actualmente se encuentra implementado un corte vertical funcional del módulo de Invitaciones, que atraviesa la interfaz web, la capa de aplicación, el dominio y la infraestructura.

## 4.2 Estilo arquitectónico seleccionado

Se selecciona un **monolito modular** como estilo arquitectónico principal.

EnAgenda se despliega como una única aplicación web, pero se organiza internamente en módulos alineados con las principales áreas del dominio:

- Eventos.
- Invitaciones.
- Tareas.
- Agenda.
- Presupuesto.
- Panel de seguimiento.

Dentro de los módulos se mantiene una separación ligera de responsabilidades entre los casos de uso de aplicación, las reglas del dominio y el acceso a infraestructura.

Esta organización busca evitar que las reglas del negocio dependan directamente de la interfaz web o de los mecanismos concretos de persistencia.

Actualmente, el módulo de Invitaciones es el que presenta el mayor nivel de implementación y constituye el corte vertical utilizado para validar la arquitectura seleccionada.

## 4.3 Límites y dependencias

Cada módulo es responsable de sus propias reglas y detalles internos.

El módulo de Invitaciones concentra actualmente responsabilidades como:

- Creación de invitaciones.
- Generación de tokens individuales.
- Definición de una fecha y hora límite de respuesta.
- Consulta de invitaciones mediante su token.
- Manejo de los estados `Pendiente`, `Confirmado` y `No asistiré`.
- Registro y actualización de la respuesta del invitado antes del vencimiento.

Los módulos no deben acceder directamente a los detalles internos de otros módulos. Cuando sea necesario intercambiar información, se utilizarán contratos o servicios explícitos dentro de la misma aplicación.

La capa de entrada web se encuentra en `app/` y está implementada con Flask.

El archivo `app/web.py` define las rutas HTTP de la aplicación, recibe las solicitudes provenientes de los formularios web y de los endpoints de la API, realiza validaciones propias de la entrada y delega las operaciones correspondientes en los casos de uso.

La presentación utiliza plantillas Jinja2 almacenadas en `app/templates/` y hojas de estilo CSS ubicadas en `app/static/css/`.

Esta capa no debe contener las reglas principales del negocio ni depender directamente de los detalles internos de persistencia.

El flujo principal implementado actualmente es:

```text
Interfaz web (HTML/CSS + Jinja2)
        ↓
Flask (app/web.py)
        ↓
GestionarInvitacion
        ↓
Invitacion / EstadoInvitacion
        ↓
RepositorioInvitacionesMemoria
```

## 4.4 Organización actual

La organización actual del código sigue el siguiente esquema general:

```text
app/
├── static/
│   └── css/
│       ├── inicio.css
│       ├── invitados.css
│       ├── invitacion.css
│       ├── invitacion_creada.css
│       └── invitaciones_creadas.css
├── templates/
│   ├── inicio.html
│   ├── invitados.html
│   ├── invitacion.html
│   ├── invitacion_creada.html
│   └── invitaciones_creadas.html
├── __init__.py
└── web.py

src/
├── agenda/
├── compartido/
├── eventos/
├── invitaciones/
│   ├── aplicacion/
│   ├── dominio/
│   └── infraestructura/
├── panel/
├── presupuesto/
└── tareas/

tests/
├── test_api_invitaciones.py
├── test_contrato_openapi.py
├── test_invitaciones.py
└── test_operacion.py
```

La carpeta `app/` actúa como punto de entrada de la aplicación web.

Dentro de `app/templates/` se encuentran las plantillas utilizadas por Flask y Jinja2 para representar las diferentes etapas del flujo de invitaciones, mientras que `app/static/css/` contiene los estilos asociados a dichas vistas.

El archivo `app/web.py` conecta la interfaz web con los casos de uso de la aplicación.

La carpeta `src/` contiene los módulos asociados al dominio de EnAgenda. El módulo `src/invitaciones/` mantiene una separación entre aplicación, dominio e infraestructura.

La carpeta `compartido/` se limita a elementos realmente transversales, evitando que se convierta en un espacio de dependencias no controladas entre los módulos.

La carpeta `tests/` contiene las pruebas automatizadas utilizadas para verificar el comportamiento del dominio, la API, el contrato OpenAPI y aspectos operativos de la aplicación.

## 4.5 Alternativas evaluadas

Se compararon los estilos de arquitectura en capas, arquitectura hexagonal y monolito modular.

La arquitectura en capas ofrece una separación técnica conocida, pero no expresa por sí sola los límites entre las áreas de negocio de EnAgenda.

La arquitectura hexagonal facilita el aislamiento frente a la infraestructura, pero introduce puertos, adaptadores e interfaces adicionales que no se justifican todavía para el alcance y las necesidades actuales del proyecto.

El monolito modular ofrece el mejor equilibrio entre separación del dominio, simplicidad de implementación, costo de despliegue y capacidad de evolución.

Durante etapas iniciales también se consideraron tecnologías y mecanismos de entrada web diferentes, como Next.js y Server Actions. Estas alternativas no forman parte de la implementación actual. La solución implementada utiliza Flask como punto de entrada web y Jinja2, HTML y CSS para la presentación.

La matriz comparativa se encuentra en:

`docs/arquitectura/matriz-comparativa-estilos.md`

La decisión completa se documenta en:

`docs/adr/0001-usar-monolito-modular.md`

## 4.6 Consecuencias actuales

### Consecuencias positivas

- Se construye, prueba y despliega una sola aplicación.
- Los módulos reflejan las áreas funcionales principales de EnAgenda.
- La interfaz web permanece separada de las reglas principales del dominio.
- El módulo de Invitaciones mantiene una separación entre aplicación, dominio e infraestructura.
- Las reglas relacionadas con tokens, vencimiento y respuestas de invitaciones se concentran en un límite identificable.
- El equipo puede distribuir el trabajo por módulos sin crear servicios independientes.
- La modularización permite considerar una futura evolución o extracción de módulos si aparece evidencia que lo justifique.
- Flask y Jinja2 permiten mantener una solución web sencilla y adecuada para el alcance actual del proyecto.

### Consecuencias asumidas

- El equipo debe respetar los límites de los módulos y evitar dependencias directas entre sus detalles internos.
- Un cambio en cualquier módulo requiere volver a construir y desplegar la aplicación completa.
- La separación interna por capas debe mantenerse ligera; crear abstracciones sin una necesidad concreta aumentaría innecesariamente la complejidad.
- La persistencia del módulo de Invitaciones se realiza actualmente mediante `RepositorioInvitacionesMemoria`, por lo que los datos no sobreviven al reinicio de la aplicación.
- La incorporación futura de persistencia permanente deberá respetar los límites establecidos entre dominio e infraestructura.
- Los límites de los módulos deberán revisarse conforme se implementen nuevas funcionalidades y aparezca nueva evidencia técnica.