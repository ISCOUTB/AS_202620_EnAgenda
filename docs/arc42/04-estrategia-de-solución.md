# 4. Estrategia de solución

## 4.1 Enfoque general

EnAgenda se desarrollará como una aplicación web responsive. Los organizadores y
los invitados accederán mediante navegador y HTTPS. Los invitados utilizarán
enlaces individuales para consultar la información permitida del evento y
registrar o actualizar su respuesta de asistencia antes de la fecha límite.

La solución se construirá como una única aplicación desplegable. Esto hace que la
complejidad operativa del proyecto sea menor y permite que un equipo de tres estudiantes
desarrolle, pruebe y despliegue el sistema sin administrar servicios
independientes.

## 4.2 Estilo arquitectónico seleccionado

Se selecciona un **monolito modular** como estilo arquitectónico principal.

EnAgenda se desplegará como una única aplicación web, pero se organizará
internamente en módulos alineados con el dominio del problema:

- Eventos.
- Invitaciones.
- Tareas.
- Agenda.
- Presupuesto.
- Panel de seguimiento.

Dentro de cada módulo se aplicará una separación ligera de responsabilidades entre
lógica de negocio, casos de uso de aplicación y acceso a infraestructura. Esta
organización busca evitar que las reglas del negocio dependan directamente de la
interfaz web o de la persistencia.

## 4.3 Límites y dependencias

Cada módulo será responsable de sus reglas y detalles internos. Por ejemplo, el
módulo de invitaciones concentrará la generación y validación de enlaces
individuales, la fecha límite de respuesta, los estados `Pendiente`,
`Confirmado` y `No asistiré`, y la actualización de la respuesta antes del
vencimiento.

Los módulos no deberán acceder directamente a los detalles internos de otros
módulos. Cuando sea necesario intercambiar información, se utilizarán contratos o
servicios explícitos dentro de la misma aplicación.

La capa de entrada web se ubicará en `app/` de Next.js e incluirá páginas,
componentes y Server Actions. Las Server Actions recibirán las solicitudes de los
formularios web y delegarán los casos de uso a los módulos correspondientes.

Esta parte no deberá contener reglas de negocio ni acceder directamente a los detalles de persistencia.

## 4.4 Organización inicial

La estructura inicial del código seguirá el siguiente esquema:

```text
app/
├── page.tsx
├── organizador/
├── invitacion/
│   └── [token]/
│       └── page.tsx
└── acciones/
    └── invitaciones.ts

src/
├── eventos/
│   ├── aplicacion/
│   ├── dominio/
│   └── infraestructura/
├── invitaciones/
│   ├── aplicacion/
│   ├── dominio/
│   └── infraestructura/
├── tareas/
│   ├── aplicacion/
│   ├── dominio/
│   └── infraestructura/
├── agenda/
│   ├── aplicacion/
│   ├── dominio/
│   └── infraestructura/
├── presupuesto/
│   ├── aplicacion/
│   ├── dominio/
│   └── infraestructura/
├── panel/
│   ├── aplicacion/
│   ├── dominio/
│   └── infraestructura/
└── compartido/
```

La carpeta `app/` actuará como punto de entrada de la aplicación web. La carpeta
`src/` contendrá los módulos del dominio. La carpeta `compartido/` se limitará a
tipos, utilidades o contratos realmente transversales para evitar que se convierta
en un lugar de dependencias no controladas.

## 4.5 Alternativas evaluadas

Se compararon los estilos de arquitectura en capas, arquitectura hexagonal y
monolito modular.

La arquitectura en capas ofrece una separación técnica conocida, pero no expresa
por sí sola los límites entre las áreas de negocio de EnAgenda. La arquitectura
hexagonal facilita el aislamiento frente a infraestructura, pero agrega puertos,
adaptadores e interfaces que no se justifican todavía para el alcance y las
necesidades actuales del proyecto.

El monolito modular ofrece el mejor equilibrio entre separación del dominio,
simplicidad de implementación, costo de despliegue y capacidad de evolución. La
matriz comparativa se encuentra en:

`docs/arquitectura/matriz-comparativa-estilos.md`

La decisión completa se documenta en:

`docs/adr/0001-usar-monolito-modular.md`

## 4.6 Consecuencias iniciales

### Consecuencias positivas

- Se construye, prueba y despliega una sola aplicación.
- Los módulos reflejan las áreas funcionales principales de EnAgenda.
- Las reglas de privacidad, vencimiento y actualización de invitaciones quedan
  concentradas en un límite identificable.
- El equipo puede distribuir trabajo por módulos sin crear servicios
  independientes.
- La modularización permite revisar una futura extracción de módulos con base en
  evidencia de implementación, carga o despliegue.

### Consecuencias asumidas

- El equipo debe respetar los límites de los módulos y evitar dependencias
  directas entre detalles internos.
- Un cambio en cualquier módulo requiere volver a desplegar la aplicación
  completa.
- La separación interna por capas debe mantenerse ligera; crear abstracciones sin
  necesidad concreta aumentaría la complejidad del proyecto.
- Los límites de los módulos se revisarán al implementar los primeros aspectos y
  pruebas del sistema.
