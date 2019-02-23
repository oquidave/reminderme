from remindme import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    apikey = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(400), index=True, unique=True)
    date = db.Column(db.DateTime())

    def __repr__(self):
        return '<Reminder {}>'.format(self.item)