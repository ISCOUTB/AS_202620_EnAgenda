# 10. Requisitos de calidad

## 10.1 Árbol de utilidad

```text
Calidad de EnAgenda
├── Seguridad y privacidad [Alta]
│   ├── Confidencialidad de invitaciones
│   │   └── Un invitado solo puede consultar la información autorizada de su invitación
│   ├── Autorización por rol y alcance
│   │   └── El propietario administra sus eventos y el invitado solo puede
│   │       consultar la información permitida y modificar su propia respuesta
│   └── Control de acceso temporal
│       └── Una invitación solo permite consultar y modificar la respuesta
│           mientras se encuentre vigente
│
├── Consistencia e integridad de datos [Alta]
│   ├── Estado único por invitación
│   │   └── Cada invitación conserva un único estado vigente
│   ├── Transiciones válidas
│   │   └── El estado solo puede cambiar mientras la invitación esté vigente
│   └── Consistencia del panel
│       └── Los conteos del panel se calculan a partir del último estado vigente
│           de cada invitación, sin contar respuestas duplicadas
│
├── Usabilidad [Alta]
│   ├── Acceso sin cuenta
│   │   └── El invitado puede responder desde un enlace sin registrarse
│   ├── Flujo comprensible
│   │   └── El invitado puede identificar el estado actual de su respuesta y
│   │       comprender el resultado después de guardarla
│   └── Facilidad para organizar
│       └── El organizador puede crear un evento y compartir invitaciones
│           sin asistencia externa
│
├── Rendimiento [Media]
│   ├── Tiempo de respuesta
│   │   └── Las operaciones principales deben responder dentro de un tiempo
│   │       definido para mantener una interacción adecuada
│   └── Capacidad de procesamiento
│       └── El sistema debe soportar la cantidad de usuarios y operaciones
│           concurrentes definida para el alcance inicial
│
└── Modificabilidad [Media]
    ├── Cambio de reglas
    │   └── Las reglas de vigencia pueden modificarse dentro del módulo
    │       correspondiente sin reescribir toda la aplicación
    └── Evolución funcional
        └── Tareas, agenda y presupuesto pueden evolucionar sin modificar
            innecesariamente la lógica interna de invitaciones y eventos
```

## 10.2 Escenarios de calidad

### EC-01 — Aislamiento entre invitaciones

| Elemento | Descripción |
|---|---|
| Fuente del estímulo | Invitado con un enlace individual válido y vigente |
| Estímulo | Intenta consultar o modificar información asociada a la invitación de otra persona |
| Artefacto | Gestión de invitaciones y control de acceso |
| Entorno | Aplicación web en funcionamiento normal |
| Respuesta | El sistema rechaza la operación y no expone información de otro invitado |
| Medida | El 100 % de los intentos incluidos en las pruebas de autorización debe ser rechazado |

### EC-02 — Vencimiento de la invitación

| Elemento | Descripción |
|---|---|
| Fuente del estímulo | Invitado con un enlace individual válido |
| Estímulo | Intenta consultar, registrar o modificar su respuesta después de la fecha y hora límite configurada para el evento |
| Artefacto | Validación de vigencia de invitaciones |
| Entorno | Aplicación web en funcionamiento normal |
| Respuesta | El sistema bloquea el acceso a la invitación, no muestra su información y presenta un mensaje de invitación cerrada |
| Medida | El 100 % de los intentos realizados después de la fecha límite debe ser bloqueado en las pruebas de vigencia |

### EC-03 — Actualización de respuesta de asistencia

| Elemento | Descripción |
|---|---|
| Fuente del estímulo | Invitado con un enlace individual vigente |
| Estímulo | Registra o cambia su estado entre `Pendiente`, `Confirmado` y `No asistiré` |
| Artefacto | Flujo público de invitación y almacenamiento de respuestas |
| Entorno | Navegador web, sin sesión autenticada y antes de la fecha límite |
| Respuesta | El sistema guarda el nuevo estado como la única respuesta vigente de la invitación y actualiza los conteos del evento |
| Medida | El 100 % de los cambios válidos incluidos en las pruebas debe actualizar el estado sin crear respuestas duplicadas |

### EC-04 — Consistencia del panel

| Elemento | Descripción |
|---|---|
| Fuente del estímulo | Propietario del evento |
| Estímulo | Consulta el panel después de que un invitado cree o actualice su respuesta antes del cierre |
| Artefacto | Panel del evento y almacenamiento de respuestas |
| Entorno | Aplicación web en funcionamiento normal |
| Respuesta | El panel muestra la cantidad correcta de invitaciones en estado `Pendiente`, `Confirmado` y `No asistiré` |
| Medida | Los conteos del panel deben coincidir con el último estado vigente de cada invitación en el 100 % de los casos de prueba |

### EC-05 — Rendimiento de operaciones principales

| Elemento | Descripción |
|---|---|
| Fuente del estímulo | Organizador o invitado |
| Estímulo | Abre una invitación vigente, registra o actualiza una respuesta, o consulta el panel del evento |
| Artefacto | Interfaz web y servicios de EnAgenda |
| Entorno | Prueba de carga inicial con hasta 10 usuarios concurrentes |
| Respuesta | El sistema procesa la operación y devuelve el resultado solicitado |
| Medida | El percentil 95 de las respuestas de las operaciones medidas debe ser menor de 2 segundos |
