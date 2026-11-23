"""Vistas de agenda y presupuesto del evento; reutiliza la sesión y CSRF de Flask."""
from flask import abort, flash, redirect, render_template, request, session, url_for
from src.agenda.aplicacion.gestionar_agenda import consultar_agenda, modificar_agenda
from src.presupuesto.aplicacion.gestionar_presupuesto import consultar_presupuesto, modificar_presupuesto


def registrar_modulos_evento(app, login_requerido):
    def mostrar(evento_id, consultar, modificar, plantilla, endpoint):
        error, codigo = None, 200
        if request.method == "POST":
            try:
                modificar(evento_id, session["usuario_id"], request.form)
            except LookupError:
                abort(404)
            except ValueError as excepcion:
                error, codigo = str(excepcion), 400
            else:
                flash("Cambios guardados correctamente.", "exito")
                return redirect(url_for(endpoint, evento_id=evento_id), code=303)
        try:
            datos = consultar(evento_id, session["usuario_id"])
        except LookupError:
            abort(404)
        return render_template(plantilla, **datos, mensaje_error=error), codigo, {"Cache-Control": "no-store"}

    @app.route("/eventos/<int:evento_id>/agenda", methods=["GET", "POST"])
    @login_requerido
    def agenda_evento(evento_id):
        return mostrar(evento_id, consultar_agenda, modificar_agenda, "agenda_evento.html", "agenda_evento")

    @app.route("/eventos/<int:evento_id>/presupuesto", methods=["GET", "POST"])
    @login_requerido
    def presupuesto_evento(evento_id):
        return mostrar(evento_id, consultar_presupuesto, modificar_presupuesto, "presupuesto_evento.html", "presupuesto_evento")
