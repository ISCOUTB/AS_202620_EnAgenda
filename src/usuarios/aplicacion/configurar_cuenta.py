"""Cambios de cuenta validados y confirmados en una sola transacción."""
import re
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from src.compartido.infraestructura.base_datos import SessionLocal
from src.usuarios.infraestructura.modelo_usuario import UsuarioModelo

TEMAS = {
    "violeta": ("Violeta", "#7052c8", "#eee9fa"),
    "rosa": ("Rosa", "#a63775", "#fbeaf3"),
    "verde": ("Verde", "#247451", "#e5f4eb"),
    "azul": ("Azul", "#2a65ae", "#e8f0fb"),
}


def configurar_cuenta(usuario_id, datos):
    accion = datos.get("accion", "")
    with SessionLocal() as sesion:
        usuario = sesion.scalar(select(UsuarioModelo).where(
            UsuarioModelo.id == usuario_id, UsuarioModelo.activo.is_(True)
        ).with_for_update())
        if usuario is None:
            raise ValueError("La cuenta no está disponible.")
        if accion == "apariencia":
            tema = datos.get("tema", "")
            if tema not in TEMAS:
                raise ValueError("Selecciona un color disponible.")
            usuario.tema = tema
        elif accion in ("perfil", "contrasena"):
            if not check_password_hash(usuario.contrasena_hash, datos.get("contrasena_actual", "")):
                raise ValueError("La contraseña actual no es correcta.")
            if accion == "perfil":
                nombre = datos.get("nombre", "").strip()
                correo = datos.get("correo", "").strip().lower()
                if not nombre or len(nombre) > 150:
                    raise ValueError("El nombre debe tener entre 1 y 150 caracteres.")
                if len(correo) > 255 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
                    raise ValueError("El correo electrónico no es válido.")
                existente = sesion.scalar(select(UsuarioModelo.id).where(
                    UsuarioModelo.correo == correo, UsuarioModelo.id != usuario_id))
                if existente is not None:
                    raise ValueError("Este correo ya está registrado.")
                usuario.nombre, usuario.correo = nombre, correo
            else:
                nueva = datos.get("nueva_contrasena", "")
                if not 8 <= len(nueva) <= 128:
                    raise ValueError("La nueva contraseña debe tener entre 8 y 128 caracteres.")
                if nueva != datos.get("confirmar_contrasena", ""):
                    raise ValueError("Las contraseñas nuevas no coinciden.")
                usuario.contrasena_hash = generate_password_hash(nueva, method="scrypt")
        else:
            raise ValueError("La operación solicitada no es válida.")
        try:
            sesion.commit()
        except IntegrityError:
            sesion.rollback()
            raise ValueError("No se pudo guardar: el correo ya está registrado.") from None
