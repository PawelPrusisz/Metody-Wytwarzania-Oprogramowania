from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask_socketio import SocketIO, send
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from .models import Inventory, User, Item, Room, Board
from . import db

import os

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/market/<first_name>', methods=['GET', 'POST'])
@login_required
def market(first_name):
    user = User.query.filter_by(first_name=first_name).first()
    return render_template("market.html", user=current_user)

@views.route('/<first_name>/<money>/<item>')
@login_required
def buy(first_name,money, item):
    print("I'm in")
    user = User.query.filter_by(first_name=first_name).first()
    user.money = user.money - int(money)
    inventoryD = Inventory.query.filter_by(id = user.id).first()
    i  = Item(name = item, author = 1, inventory_id = user.id)
    print("Item: ", i)
    print("inventoryD owner", inventoryD.owner)
    print("inventoryD items", inventoryD.items)
    for c in inventoryD.items:
        print("d", c.name)

    db.session.add(i)
    db.session.commit()
    return redirect("/market/"+first_name)

@views.route('/chat')
def chat():
    return render_template('chat.html')

@views.route('/game', methods=['GET', 'POST'])
def game():
    if(request.method=='POST'):
        user = User.query.filter_by(email= current_user.email).first()
        session['username'] = user.first_name
        return render_template('game.html', user=current_user)
    else:
        if(session.get('username') is not None):
            user = User.query.filter_by(email= current_user.email).first()
            inventoryD = Inventory.query.filter_by(id = user.id).first()

            return render_template('game.html', user=current_user, inventory= inventoryD)


@views.route("/inventory/<first_name>")
@login_required
def inventory(first_name):
    user = User.query.filter_by(first_name=first_name).first()
    if not user:
        flash('No user with that usernamerexists.', category='error')
        return redirect(url_for('views.home'))

    inventory = user.inventory
    return render_template("inventory.html", user=current_user, inventory=inventory, first_name=first_name)


@views.route('/test')
def test():
    return render_template('test.html', user=current_user)





