from flask import Blueprint, render_template, request
from datetime import datetime
from .models import Event
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def landing():
    q      = (request.args.get('q') or '').strip()
    when   = (request.args.get('when') or 'upcoming').lower()
    status = (request.args.get('status') or 'all').lower()

    query = Event.query

    # free-text search (title or description)
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Event.title.ilike(like), Event.description.ilike(like))
        )

    # when filter
    now = datetime.now()
    if when == 'upcoming':
        query = query.filter(Event.start_date >= now)
    elif when == 'past':
        query = query.filter(Event.start_date < now)
    # (when == 'all' → no filter)

    # status filter (change the right side to match your column’s values)
    if status != 'all':
        status_map = {'open': 'Open', 'soldout': 'Sold Out', 'inactive': 'Inactive'}
        query = query.filter(Event.availability == status_map.get(status, 'Open'))

    events = query.order_by(Event.start_date.asc()).all()
    return render_template('index.html', events=events, q=q, when=when, status=status)


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

