# Aspectos

| ID | Aspecto | Requisito | C4 | ADR | Código | Pruebas | Evidencia |
|---|---|---|---|---|---|---|---|
<<<<<<< HEAD

| A-01 | Gestión de Invitaciones | El sistema debe permitir al propietario generar un enlace individual para cada invitado, mediante el cual el invitado pueda consultar la información pública del evento y registrar su respuesta de asistencia. | [C4 Nivel 1](c4/nivel-1-contexto.md)<br>[C4 Nivel 2](c4/nivel-2-contenedores.md)<br>[C4 Nivel 3](c4/nivel-3-componentes.md) | [ADR-0001](adr/0001-usar-monolito-modular.md) | [Aplicación Flask](../app/web.py)<br>[Gestión de invitación](../src/invitaciones/aplicacion/gestionar_invitacion.py)<br>[Dominio de invitaciones](../src/invitaciones/dominio/invitaciones.py)<br>[Repositorio en memoria](../src/invitaciones/infraestructura/repositorio_memoria.py) | [Pruebas de invitaciones](../tests/test_invitaciones.py) | [README del proyecto](../README.md) |
=======
| A-01 | Gestión de invitaciones | El sistema debe permitir al propietario generar un enlace individual para cada invitado. El invitado podrá consultar la información autorizada y registrar o actualizar su respuesta entre `Pendiente`, `Confirmado` y `No asistiré` mientras el enlace esté vigente. Después de la fecha límite, el enlace no permitirá consultar ni modificar la invitación. | C4 nivel 1 y nivel 2 de EnAgenda | `docs/adr/0001-usar-monolito-modular.md` | `src/invitaciones/` | `tests` | Pendiente |
>>>>>>> 13fdc8ea8a9bc015c10b3299260a005fbc91eb1e
