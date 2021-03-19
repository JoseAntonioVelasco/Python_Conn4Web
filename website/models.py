from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.String(150))
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #define relationships
    user1 = db.relationship("User", foreign_keys=[user1_id])
    user2 = db.relationship("User", foreign_keys=[user2_id])

    moves = db.relationship('Move')

class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_match = db.Column(db.Integer, db.ForeignKey('match.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    pos = db.Column(db.String(150), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


