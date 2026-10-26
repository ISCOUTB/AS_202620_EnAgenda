# C4 — Nivel 2: Contenedores

```mermaid
C4Container
    title EnAgenda — contenedores actuales
    Person(organizador, "Organizador", "Administra sus eventos")
    Person(invitado, "Invitado", "Consulta y responde su invitación")
    System_Boundary(sistema, "EnAgenda") {
        Container(web, "Aplicación web", "Python / Flask / Gunicorn", "HTML, API y módulos de negocio; almacén heredado y métricas en memoria del proceso")
        ContainerDb(db, "Base de datos", "PostgreSQL 17", "Usuarios, eventos e invitaciones persistentes; volumen postgres_data")
    }
    Rel(organizador, web, "Administra", "HTTP / HTML")
    Rel(invitado, web, "Consulta y responde", "HTTP / HTML o JSON heredado")
    Rel(web, db, "Lee y confirma transacciones", "SQL / psycopg / SQLAlchemy")
```

Los módulos Python son componentes internos de Flask, no contenedores desplegables.
La memoria heredada vive dentro de cada worker; no es una base compartida ni caché.
No se despliegan broker ni caché de negocio. PostgreSQL y Flask corresponden a los
servicios `db` y `enagenda` de `docker-compose.yml`.
