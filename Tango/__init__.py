from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
from flask_login import LoginManager

db = SQLAlchemy()


#initalises the application
def create_app():
    app=Flask(__name__)
    app.debug = True
    app.secret_key = 'TangoSecret3254'


    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tango.db'

    from . import models
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # init_tables() used on first startup to init some tables 


    login_manager = LoginManager()
    

    login_manager.login_view = 'auth.login'
    login_manager.login_message = "You must be a logged in user to access that page"
    login_manager.init_app(app)
    
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .views import mainbp
    app.register_blueprint(mainbp)

    from .auth import bd
    app.register_blueprint(bd)


    return app
