# 10. Requisitos de calidad

## 10.1 Árbol de utilidad

```text
Utilidad de EnAgenda
├── Privacidad y seguridad [Alta]
│   ├── Un invitado solo puede acceder a la información asociada a su propia invitación
│   ├── Los enlaces individuales no permiten acceder a información de otros invitados
│   ├── El enlace deja de estar disponible después de la fecha límite de respuesta
│   └── Solo el propietario puede administrar la información del evento
├── Usabilidad [Alta]
│   ├── El organizador puede crear y compartir un evento desde una aplicación web
│   ├── El invitado puede responder sin instalar una aplicación ni crear una cuenta
│   └── El invitado puede cambiar su respuesta antes de la fecha límite
├── Consistencia [Alta]
│   ├── Cada invitación conserva un único estado vigente:
│   │   Pendiente, Confirmado o No asistiré
│   ├── El invitado puede actualizar su estado antes del vencimiento
│   └── El panel refleja los conteos correctos según el último estado vigente
├── Rendimiento [Media]
│   ├── La consulta de una invitación vigente responde rápidamente
│   ├── El registro o actualización de una respuesta se procesa rápidamente
│   └── El panel del evento responde en un tiempo aceptable
└── Modificabilidad [Media]
    ├── Las funciones de invitados, tareas, agenda y presupuesto pueden evolucionar
    │   sin afectar indiscriminadamente las demás funciones
    └── Las reglas de acceso y vencimiento pueden ajustarse sin reescribir la
        aplicación completa
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
