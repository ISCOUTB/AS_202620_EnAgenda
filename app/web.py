import os
import sys

# Permite importar el paquete src cuando ejecutamos:
# python app\web.py
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from datetime import datetime

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    send_file,
)

from src.invitaciones.aplicacion.gestionar_invitacion import GestionarInvitacion
from src.invitaciones.dominio.invitaciones import EstadoInvitacion
from src.invitaciones.infraestructura.repositorio_memoria import (
    RepositorioInvitacionesMemoria,
)


app = Flask(__name__)

# Repositorio en memoria para la interfaz mínima
repositorio = RepositorioInvitacionesMemoria()
gestionar_invitacion = GestionarInvitacion(repositorio)

# Métricas básicas de observabilidad HTTP
http_requests_total = 0
http_requests_by_path = {}
http_responses_by_status = {}

# Métrica específica de consultas de invitaciones
invitaciones_consultadas_total = 0

@app.before_request
def registrar_peticion():
    global http_requests_total

    # Evita que consultar /metrics altere sus propias métricas
    if request.path == "/metrics":
        return

    http_requests_total += 1

    http_requests_by_path[request.path] = (
        http_requests_by_path.get(request.path, 0) + 1
    )


@app.after_request
def registrar_respuesta(response):
    if request.path == "/metrics":
        return response

    codigo = str(response.status_code)

    http_responses_by_status[codigo] = (
        http_responses_by_status.get(codigo, 0) + 1
    )

    return response


@app.get("/health")
def health():
    return {
        "service": "enagenda-api",
        "status": "ok"
    }, 200


@app.get("/metrics")
def metrics():
    """Expone las métricas de observabilidad de EnAgenda."""
    return jsonify(
        {
            "metric": "enagenda_invitaciones_consultadas_total",
            "value": invitaciones_consultadas_total,
            "description": "Total de consultas de invitaciones realizadas",
            "http_requests_total": http_requests_total,
            "http_requests_by_path": http_requests_by_path,
            "http_responses_by_status": http_responses_by_status,
        }
    ), 200


@app.get("/openapi.yaml")
def obtener_contrato_openapi():
    ruta_contrato = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "docs",
        "api",
        "openapi.yaml",
    )

    return send_file(
        ruta_contrato,
        mimetype="application/yaml",
    )


@app.route("/", methods=["GET", "POST"])
def inicio():
    """Muestra el inicio de EnAgenda y permite crear invitaciones."""
    mensaje_error = None

    if request.method == "POST":
        destinatario = request.form.get("destinatario", "").strip()
        fecha_limite = request.form.get("fecha_limite", "").strip()

        if not destinatario:
            mensaje_error = "Debes ingresar el nombre del invitado."

        elif not fecha_limite:
            mensaje_error = "Debes seleccionar una fecha límite."

        else:
            try:
                fecha_limite_respuesta = datetime.fromisoformat(fecha_limite)

                if fecha_limite_respuesta <= datetime.now():
                    mensaje_error = (
                        "La fecha límite debe ser posterior a la fecha actual."
                    )
                else:
                    invitacion = gestionar_invitacion.crear_invitacion(
                        destinatario=destinatario,
                        fecha_limite_respuesta=fecha_limite_respuesta,
                    )

                    return redirect(
                        url_for(
                            "ver_invitacion",
                            token=invitacion.token,
                        )
                    )

            except ValueError:
                mensaje_error = "La fecha ingresada no es válida."

    return render_template(
        "inicio.html",
        mensaje_error=mensaje_error,
    )


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
            nuevo_estado = None

        if nuevo_estado is None:
            mensaje = "Estado no válido."
        else:
            try:
                gestionar_invitacion.responder(
                    token=token,
                    estado=nuevo_estado,
                    ahora=datetime.now(),
                )
                mensaje = "Respuesta registrada correctamente."
            except ValueError as error:
                return f"<h1>Error</h1><p>{error}</p>", 404

    try:
        invitacion = gestionar_invitacion.consultar(
            token=token,
            ahora=datetime.now(),
        )
    except ValueError as error:
        return f"<h1>Error</h1><p>{error}</p>", 404

    return render_template(
    "invitacion.html",
    invitacion=invitacion,
    mensaje=mensaje,
)


@app.route("/api/v1/invitaciones/<token>", methods=["GET"])
def api_consultar_invitacion(token):
    """Consulta una invitación y devuelve sus datos en JSON."""
    global invitaciones_consultadas_total

    try:
        invitacion = gestionar_invitacion.consultar(
            token=token,
            ahora=datetime.now(),
        )
        invitaciones_consultadas_total += 1
    except ValueError as error:
        return jsonify(
            {
                "error": str(error)
            }
        ), 404
    
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

    if not isinstance(datos, dict) or "estado" not in datos:
        return jsonify(
            {
                "error": "Debe proporcionar el campo 'estado'."
            }
        ), 400

    estado = datos["estado"]

    if estado == "confirmado":
        nuevo_estado = EstadoInvitacion.CONFIRMADO
    elif estado == "no_asistire":
        nuevo_estado = EstadoInvitacion.NO_ASISTIRE
    else:
        return jsonify(
            {
                "error": "El estado proporcionado no es válido."
            }
        ), 400

    try:
        invitacion = gestionar_invitacion.responder(
            token=token,
            estado=nuevo_estado,
            ahora=datetime.now(),
        )
    except ValueError as error:
        return jsonify(
            {
                "error": str(error)
            }
        ), 404

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