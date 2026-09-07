# Aspectos

| ID | Aspecto | Requisito | C4 | ADR | Código | Pruebas | Evidencia |
|---|---|---|---|---|---|---|---|
| A-01 | Gestión de Invitaciones | El sistema debe permitir al propietario generar un enlace individual para cada invitado, mediante el cual el invitado pueda consultar la información pública del evento y registrar su respuesta de asistencia. | [C4 Nivel 1](c4/nivel-1-contexto.md)<br>[C4 Nivel 2](c4/nivel-2-contenedores.md) | [ADR-0001](adr/0001-usar-monolito-modular.md) | [Módulo de invitaciones](../src/invitaciones/)<br>[Aplicación](../app/web.py) | [Pruebas de invitaciones](../tests/test_invitaciones.py) | [Correcciones al feedback](/docs/evidencia.md)|