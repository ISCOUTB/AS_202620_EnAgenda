# 0001 - Aplicación móvil y página web para invitaciones

- Estado: propuesto
- Fecha: 2026-08-08
- Decide: Equipo del proyecto
- Escenario relacionado: EC-01

## Contexto

El propietario administrará los eventos desde una aplicación móvil. Los
invitados podrán consultar y responder sus invitaciones desde una página web,
sin registrarse ni instalar la aplicación.

## Alternativas consideradas

### A. Aplicación móvil para todos

Se descarta porque obligaría a los invitados a instalar la aplicación.

### B. Aplicación web completa

Se mantiene como alternativa, pero inicialmente se prioriza una experiencia
móvil para el propietario.

### C. Aplicación móvil y página web para invitaciones

Se propone utilizar una aplicación móvil para el propietario y una página web
pública para los invitados.

## Consecuencias positivas

- Los invitados no necesitan instalar la aplicación.
- Se dispone de una URL pública.
- Se separa la información privada de la pública.

## Consecuencias negativas

- Se deben mantener una aplicación móvil y una página web.
- Se deben probar dos clientes diferentes.
- La API debe limitar la información pública de las invitaciones.
