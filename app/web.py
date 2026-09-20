
import os
import sys

# Permite importar el paquete src cuando ejecutamos:
# python app\web.py
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from datetime import datetime, timedelta

from flask import Flask, jsonify, redirect, render_template_string, request, url_for

from src.invitaciones.aplicacion.gestionar_invitacion import GestionarInvitacion
from src.invitaciones.dominio.invitaciones import EstadoInvitacion
from src.invitaciones.infraestructura.repositorio_memoria import (
    RepositorioInvitacionesMemoria,
)


app = Flask(__name__)

# Repositorio en memoria para la interfaz mínima
repositorio = RepositorioInvitacionesMemoria()
gestionar_invitacion = GestionarInvitacion(repositorio)


@app.route("/")
def inicio():
    """Crea una invitación de prueba y muestra su página."""
    invitacion = gestionar_invitacion.crear_invitacion(
        destinatario="Invitado de prueba",
        fecha_limite_respuesta=datetime.now() + timedelta(days=1),
    )

    return redirect(url_for("ver_invitacion", token=invitacion.token))


@app.route("/invitacion/<token>", methods=["GET", "POST"])
def ver_invitacion(token):
    """Muestra una invitación y permite responderla."""
    mensaje = None

    if request.method == "POST":
        estado = request.form.get("estado")

        if estado == "confirmado":
            nuevo_estado = EstadoInvitacion.CONFIRMADO
        elif estado == "no_asistire":
            nuevo_estado = EstadoInvitacion.NO_ASISTIRE
        else:
            mensaje = "Respuesta no válida."
            nuevo_estado = None

        if nuevo_estado is not None:
            try:
                invitacion = gestionar_invitacion.responder(
                    token=token,
                    estado=nuevo_estado,
                    ahora=datetime.now(),
                )

                mensaje = (
                    f"Respuesta guardada: "
                    f"{invitacion.estado.value}"
                )

            except ValueError as error:
                mensaje = str(error)

    try:
        invitacion = gestionar_invitacion.consultar(
            token=token,
            ahora=datetime.now(),
        )

    except ValueError as error:
        return f"<h1>Error</h1><p>{error}</p>", 404

    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Invitación - EnAgenda</title>
        </head>

        <body>
            <h1>EnAgenda</h1>

            <h2>Invitación</h2>

            <p>
                <strong>Destinatario:</strong>
                {{ invitacion.destinatario }}
            </p>

            <p>
                <strong>Estado:</strong>
                {{ invitacion.estado.value }}
            </p>

            <p>
                <strong>Fecha límite:</strong>
                {{ invitacion.fecha_limite_respuesta }}
            </p>

            {% if mensaje %}
                <p>
                    <strong>{{ mensaje }}</strong>
                </p>
            {% endif %}

            <form method="post">
                <button
                    type="submit"
                    name="estado"
                    value="confirmado"
                >
                    Confirmar asistencia
                </button>

                <button
                    type="submit"
                    name="estado"
                    value="no_asistire"
                >
                    No asistiré
                </button>
            </form>
        </body>
        </html>
        """,
        invitacion=invitacion,
        mensaje=mensaje,
    )

@app.route("/api/v1/invitaciones/<token>", methods=["GET"])
def api_consultar_invitacion(token):
    """Consulta una invitación y devuelve sus datos en JSON."""
    try:
        invitacion = gestionar_invitacion.consultar(
            token=token,
            ahora=datetime.now(),
        )

    except ValueError as error:
        return jsonify({"error": str(error)}), 404

    return jsonify(
        {
            "token": invitacion.token,
            "destinatario": invitacion.destinatario,
            "fecha_limite_respuesta": (
                invitacion.fecha_limite_respuesta.isoformat()
            ),
            "estado": invitacion.estado.value,
        }
    ), 200


@app.route("/api/v1/invitaciones/<token>", methods=["POST"])
def api_responder_invitacion(token):
    """Registra la respuesta del invitado y devuelve la invitación en JSON."""
    datos = request.get_json(silent=True)

    if not datos or "estado" not in datos:
        return jsonify(
            {"error": "Debe proporcionar el campo 'estado'."}
        ), 400

    estado = datos["estado"]

    if estado == "confirmado":
        nuevo_estado = EstadoInvitacion.CONFIRMADO
    elif estado == "no_asistire":
        nuevo_estado = EstadoInvitacion.NO_ASISTIRE
    else:
        return jsonify(
            {"error": "El estado proporcionado no es válido."}
        ), 400

    try:
        invitacion = gestionar_invitacion.responder(
            token=token,
            estado=nuevo_estado,
            ahora=datetime.now(),
        )

    except ValueError as error:
        return jsonify({"error": str(error)}), 404

    return jsonify(
        {
            "token": invitacion.token,
            "destinatario": invitacion.destinatario,
            "fecha_limite_respuesta": (
                invitacion.fecha_limite_respuesta.isoformat()
            ),
            "estado": invitacion.estado.value,
        }
    ), 200


if __name__ == "__main__":
    app.run(debug=True)

