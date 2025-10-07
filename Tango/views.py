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
