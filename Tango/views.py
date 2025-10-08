from flask import Blueprint, render_template
from .forms import LoginForm

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

@mainbp.route('/login')
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return render_template('/')
    return render_template('Login.html', form=login_form)

@mainbp.route('/signup')
def signup():
    return render_template('SignUp.html')

