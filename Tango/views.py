from flask import Blueprint, render_template, request, session, redirect, url_for
from .forms import LoginForm, SignUpForm, EventManagement

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def landing():
    return render_template('index.html')

@mainbp.route('/managment')
def eventManagment():
    Event_Management_form = EventManagement()
    if Event_Management_form.validate_on_submit():
        return render_template('/')

    return render_template('event_managment.html', form=Event_Management_form)

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
    SignUp_form = SignUpForm()
    if SignUp_form.validate_on_submit():
        return render_template('/')

    return render_template('SignUp.html', form=SignUp_form)

