from . import db
from flask_login import UserMixin

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default='/static/img/casual-img.jpg')
    availability = db.Column(db.Integer, nullable=False) # number of tickets 
    status = db.Column(db.String(64), index=True, nullable=False)# Available, low-availability, sold out
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(20), nullable=False)
    catagory = db.Column(db.String(60), nullable=False, default="No Category") # casual, competative, social
    location = db.Column(db.String(500), nullable=False)

    host = db.Column(db.Integer, db.ForeignKey('users.id'))

    tickets = db.relationship('Ticket', backref='event')
    comments = db.relationship('Comment', backref='event') 

    def __repr__(self):
        return "title: {}, description {}, id {},".format(self.title, self.description, self.id)

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), nullable=False, default='Active') # Active, Inactive
    purchase_date = db.Column(db.Date, nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __repr__(self):
        return "status: {}, purchased {}, id {}".format(self.status, self.purchase_date, self.id)
    
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id')) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "by {}, at {}, for{}".format(self.user_id, self.date_posted, self.event_id)

class User(db.Model, UserMixin):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(64), nullable=False)

    ticket = db.relationship('Ticket', backref='user')
    comments = db.relationship('Comment', backref='user')
    hosted_events = db.relationship('Event', backref='host_user', foreign_keys='Event.host')

    def __repr__(self):
        return "name: {}, email {}, comments {}".format(self.first_name, self.email, self.password_hash)
    