# errors.py
from flask import Blueprint, render_template, current_app

errorsbp = Blueprint("errors", __name__)

@errorsbp.app_errorhandler(404)
def not_found(e):
    # Render a friendly page for unknown routes
    return render_template("errors/404.html"), 404

@errorsbp.app_errorhandler(500)
def internal_error(e):
    # Log the stack trace so devs can see it in the console/logs
    current_app.logger.exception("Unhandled exception: %s", e)
    return render_template("errors/500.html"), 500
