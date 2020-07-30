from datetime import datetime
from mindful import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teams_id = db.Column(db.String(36), nullable=False, unique=True)
    moods = db.relationship('Mood', backref='author', lazy=True)

    def __init__(self, id, teams_id):
       self.id = id
       self.teams_id = teams_id
       pass

    @property
    def serialize(self):
        return {'id': self.id, 'teams_id': self.teams_id}

    def __repr__(self):
        return "{self.id}"


class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    content = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "{self.id} {self.rating}"
