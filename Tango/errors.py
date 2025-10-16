from flask import Blueprint, render_template

errorsbp = Blueprint('errors', __name__)

@errorsbp.app_errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@errorsbp.app_errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500
