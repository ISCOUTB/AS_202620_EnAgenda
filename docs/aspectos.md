# Aspectos

| ID | Aspecto | Requisito | C4 | ADR | Código | Pruebas | Evidencia |
|---|---|---|---|---|---|---|---|
| A-01 | Gestión de invitaciones | El sistema debe permitir al propietario generar un enlace individual para cada invitado. El invitado podrá consultar la información autorizada y registrar o actualizar su respuesta entre `Pendiente`, `Confirmado` y `No asistiré` mientras el enlace esté vigente. Después de la fecha límite, el enlace no permitirá consultar ni modificar la invitación. | C4 nivel 1 y nivel 2 de EnAgenda | `docs/adr/0001-usar-monolito-modular.md` | `src/invitaciones/` | `tests` | Pendiente |
