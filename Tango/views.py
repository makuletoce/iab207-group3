from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from .forms import EventManagement, TicketForm, CommentForm
from .models import Ticket, Event, Comment
from flask_login import login_required, current_user
from . import db
from datetime import date
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
import os
from werkzeug.utils import secure_filename

mainbp = Blueprint('main', __name__)

@mainbp.route('/search')
def search():

    banner_events = Event.query.all()

    q = request.args.get('q', '').strip()

    if not q:
        return redirect(url_for('main.landing'))

    results = (
        Event.query.filter(
            Event.title.ilike(f"%{q}%") |
            Event.description.ilike(f"%{q}%") |
            Event.location.ilike(f"%{q}%") |
            Event.catagory.ilike(f"%{q}%")
        ).all()
    )

    return render_template('index.html', events=results, search_query=q, banner_events = banner_events)



@mainbp.route('/', methods=['GET','POST'])
def landing():

    banner_events = Event.query.all()

    catagory_filters = request.args.getlist('catagory')
    availability_filters = request.args.getlist('availability')

    query = Event.query

    filters = []
    if availability_filters:
        filters.append(Event.status.in_(availability_filters))
        
    if catagory_filters:
        filters.append(Event.catagory.in_(catagory_filters))

    if filters:
        events = query.filter(or_(*filters)).all()

    else:
        events = Event.query.all()
    return render_template('index.html', events=events, banner_events= banner_events)



@mainbp.route('/managment', defaults={'event_id': None}, methods=['GET', 'POST'])
@mainbp.route('/managment/<int:event_id>', methods=['GET', 'POST'])
@login_required
def eventManagment(event_id):

    user_events = Event.query.filter_by(host=current_user.id).all()
    
    if event_id is None :
        form = EventManagement()
        if form.validate_on_submit():
            if form.image.data:
                filename = secure_filename(form.image.data.filename)
                img_path = os.path.join(current_app.root_path, 'static', 'img', filename)
                form.image.data.save(img_path)
            else:
                filename = 'casual-image.jpg'

            new_event = Event(title = form.event_name.data,
                            description = form.description.data,
                            date = form.event_date.data,
                            time = form.event_time.data,
                            location = form.location.data,
                            catagory = form.catagory.data,
                            availability = form.num_of_tickets.data,
                            host = current_user.id,
                            image = filename
                            )
            
            db.session.add(new_event)
            db.session.commit()

            return redirect(url_for("main.landing"))
        
    # if user is editing an event
    else:
        event = Event.query.filter_by(id=event_id).first()
        form = EventManagement(obj=event)

        if form.validate_on_submit():
           
           #if event is canceled
           if form.cancel.data:
               event.status = "Canceled"
               db.session.commit()
               flash('Event Canceled')
               return redirect(url_for('main.landing'))
           
           #add edited data to database
           else:
            event.title = form.title.data
            event.description = form.description.data
            event.date  = form.date.data
            event.time = form.time.data
            event.location = form.location.data
            event.catagory = form.catagory.data
            event.availability = form.availability.data
            event.host = current_user.id

            db.session.commit()
            flash('Event Updated')
            return redirect(url_for('main.landing'))             

    return render_template('event_managment.html', events=user_events, form=form, event_id=event_id)

@mainbp.route('/history')
@login_required
def eventHistory():
    # pass all tickets of the logged in user to the page
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('booking_history.html', tickets=tickets)

@mainbp.route('/details/<int:event_id>', methods=['GET', 'POST'] )
def eventDetails(event_id):

    # get event id from url
    event = Event.query.get_or_404(event_id)
    form = TicketForm()
    comment_form = CommentForm()
    error = None

    # pull comments for this event and eager-load each comment's user
    comments = (
        Comment.query
        .options(joinedload(Comment.user))        # so c.user is usable in the template
        .filter_by(event_id=event.id)
        .order_by(Comment.date_posted.desc())
        .all()
    )

    if comment_form.validate_on_submit() and comment_form.submit_comment.data:
        if not current_user.is_authenticated:
            flash("You need to be logged in to comment!")
            return redirect(url_for("auth.login"))
        
        new_comment = Comment(
            comment=comment_form.comment.data,
            event_id=event.id,
            user_id=current_user.id,
            date_posted=date.today()
        )
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment posted successfully!")
        return redirect(url_for('main.eventDetails', event_id=event.id))
    
    if form.validate_on_submit():
        
        # if not logged in
        if  not current_user.is_authenticated:
            error="You need to be logged in to attend events"
            flash(error)
            return redirect(url_for("auth.login"))
        
        elif event.availability < form.quantity.data:
            error="There are not enough tickets to complete Purchase"
        
        # make a new ticket for the amount of tickets ordered
        else:
            event.availability = event.availability - form.quantity.data
            for new_ticket in range(form.quantity.data):
                new_ticket = Ticket(purchase_date = date.today(),
                                    event_id = event.id,
                                    user_id = current_user.id)
                db.session.add(new_ticket)
            db.session.commit()
            return redirect(url_for("main.landing"))
            
    return render_template('event_details.html', event=event, form=form, comment_form=comment_form, comments=comments, error=error)
