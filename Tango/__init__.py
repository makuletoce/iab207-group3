from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
from flask_login import LoginManager
from flask import Flask, render_template

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

    @app.errorhandler(404)
    def not_found(e):
        print(">>> 404 handler hit")
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        try:
            db.session.rollback()
        except Exception:
            pass
        print(">>> 500 handler hit")
        return render_template('errors/500.html'), 500

    from .auth import bd
    app.register_blueprint(bd)


    return app


def init_tables():
    from .models import User, Event, Ticket

    jim = User(first_name="jim", 
                        last_name="gray",
                        phone_number="0487293323", 
                        email="jimGray@hotmail.com", 
                        password_hash="notmypassword",
                        address="nottelling, grov")
    
    tim = User(first_name="tim", 
                        last_name="yarg",
                        phone_number="0433283729", 
                        email="TimTim@gmail.com", 
                        password_hash="mypassword",
                        address="13 tellem, close")
    
    event = Event(title ="friend slop",
                  date = date.today(),
                  time = "1:30pm",
                  location = "31 roundtime ave",
                  catagory = "Social",
                  description = "come down and enjoy some quality time with some new friends",
                  host = 1,       
                  availability = 30,
                  status = "Available"
                  )
    
    ticket = Ticket(purchase_date = datetime.now(),
                    event_id = 1,
                    user_id = 2)
    
    db.session.add(jim)
    db.session.add(tim)
    db.session.add(event)
    db.session.add(ticket)
    db.session.commit()