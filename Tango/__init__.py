from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


#initalises the application
def create_app():
    app=Flask(__name__)
    app.debug = True
    app.secret_key = 'TangoSecret3254'


    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tango.db'

    from . import models
    db.init_app(app)

    # with app.app_context():
    #     db.create_all()

    from .views import mainbp
    app.register_blueprint(mainbp)

    return app