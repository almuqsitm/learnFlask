import pytz
from . import db
from flask_login import UserMixin
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, data, user_id, date=None):
        self.data = data
        self.user_id = user_id
        if date is None:
            est_tz = pytz.timezone('America/New_York')
            est_now = datetime.now(est_tz).replace(microsecond=0)
            self.date = est_now
        else:
            self.date = date.replace(microsecond=0)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')