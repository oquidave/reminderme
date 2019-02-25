from remindme import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    apikey = db.Column(db.String(120), index=True, unique=True)
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    reminders = db.relationship('Reminder', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(400), index=True, unique=True)
    due_date = db.Column(db.DateTime())
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Reminder {}>'.format(self.item)