from flask import Blueprint, render_template, url_for

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def landing():
    return render_template('index.html')

@mainbp.route('/managment')
def eventManagment():
    return render_template('event_managment.html')

@mainbp.route('/history')
def eventHistory():
    return render_template('booking_history.html')

@mainbp.route('/details')
def eventDetails():
    return render_template('event_details.html')
<<<<<<< HEAD:main.py

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/signup')
def signup():
    return render_template('SignUp.html')


app.run()
=======
>>>>>>> 54350c9a5ba1453e5e23df25ad497378e8202b0e:Tango/views.py
