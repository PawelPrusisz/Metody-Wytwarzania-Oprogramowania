from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    money = db.Column(db.Integer)
    inventory = db.relationship('Inventory', backref='user', passive_deletes=True)
    items = db.relationship('Item', backref='user', passive_deletes=True)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.String(150))
    user = db.Column(db.String(150))

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    boardState = db.Column(db.JSON)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    items = db.relationship('Item', backref='post', passive_deletes=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey(
        'inventory.id', ondelete="CASCADE"), nullable=False)