from . import db 
from flask_login import UserMixin 
from sqlalchemy.sql import func 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    music = db.relationship('Music')

class Music(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_name = db.Column(db.String(150))