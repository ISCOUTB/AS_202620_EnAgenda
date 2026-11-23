import os
import smtplib
import ssl
from email.message import EmailMessage
from html import escape
from urllib.parse import urlsplit


def enviar_invitaciones_por_correo(invitaciones, titulo_evento):
    """Envía invitaciones ya guardadas; devuelve cantidades sin exponer secretos."""
    enviadas = 0
    fallidas = 0

    try:
        base_url = os.environ["APP_BASE_URL"].strip().rstrip("/")
        direccion = urlsplit(base_url)

        if direccion.scheme not in ("http", "https") or not direccion.netloc:
            raise ValueError("APP_BASE_URL no es válida.")

        usuario = os.environ["MAIL_SMTP_USER"]
        contrasena = os.environ["MAIL_SMTP_PASSWORD"].replace(" ", "")
        remitente = os.environ["MAIL_FROM"]
        host = os.environ["MAIL_SMTP_HOST"]
        puerto = int(os.environ["MAIL_SMTP_PORT"])

        with smtplib.SMTP(host, puerto, timeout=10) as smtp:
            smtp.ehlo()
            smtp.starttls(context=ssl.create_default_context())
            smtp.ehlo()
            smtp.login(usuario, contrasena)

            for invitacion in invitaciones:
                try:
                    enlace = (
                        f"{base_url}/eventos/invitacion/"
                        f"{invitacion['token']}"
                    )

                    mensaje = EmailMessage()
                    mensaje["Subject"] = "Tienes una invitación en EnAgenda"
                    mensaje["From"] = remitente
                    mensaje["To"] = invitacion["correo"]

                    mensaje.set_content(
                        f"Hola, {invitacion['nombre']}.\n\n"
                        f"Te han invitado a: {titulo_evento}.\n"
                        f"Consulta los detalles y responde aquí:\n{enlace}\n\n"
                        "Este enlace es personal. No lo compartas."
                    )

                    mensaje.add_alternative(
                        f"""\
<!DOCTYPE html>
<html lang="es">
<body>
    <h1>Has recibido una invitación</h1>
    <p>Hola, {escape(invitacion['nombre'])}.</p>
    <p>Te han invitado a <strong>{escape(titulo_evento)}</strong>.</p>
    <p>Consulta los detalles del evento y confirma tu asistencia:</p>
    <p>
        <a href="{escape(enlace, quote=True)}"
           style="display:inline-block;padding:12px 20px;
                  background:#2563eb;color:#ffffff;
                  text-decoration:none;border-radius:6px;">
            Ver invitación
        </a>
    </p>
    <p>Este enlace es personal. No lo compartas.</p>
    <p>EnAgenda</p>
</body>
</html>
""",
                        subtype="html",
                    )

                    smtp.send_message(mensaje)
                    enviadas += 1

                except (smtplib.SMTPException, OSError, ValueError):
                    fallidas += 1

    except (KeyError, ValueError, OSError, smtplib.SMTPException):
        fallidas = len(invitaciones) - enviadas

    return {"enviadas": enviadas, "fallidas": fallidas}