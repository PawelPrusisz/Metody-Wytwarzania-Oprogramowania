from website import create_app
from flask_socketio import SocketIO, send
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from website import models
from website import db
from flask_login import login_required, current_user




app = create_app()
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    #app.run(debug=True)
    app.config['SESSION_TYPE'] = 'filesystem'

    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.html')

    @app.route('/chat', methods=['GET', 'POST'])
    @login_required
    def chat():
        if(request.method=='POST'):
            user = models.User.query.filter_by(email= current_user.email).first()
            print(user)
            print(user.first_name)
            print(user.email)
            print(current_user.email)
            room = "Main Hole"
            #Store the data in session
            session['username'] = user.first_name
            session['room'] = room
            msg = models.Room.query.filter_by()
            messages = []

            for i in msg:
                print(i.comments, i.user)
                messages.append(i.user + " : " + i.comments)

            return render_template('chat.html', session = session,  messages =  messages)
        else:
            if(session.get('username') is not None):
                return render_template('chat.html', session = session)
            else:
                return redirect(url_for('index'))

    @socketio.on('join', namespace='/chat')
    def join(message):
        room = session.get('room')
        join_room(room)
        emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


    @socketio.on('text', namespace='/chat')
    def text(message):
        room = session.get('room')

        m = models.Room(comments = message['msg'], user= current_user.first_name)
        db.session.add(m)
        db.session.commit()

        emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


    @socketio.on('left', namespace='/chat')
    def left(message):
        room = session.get('room')
        username = session.get('username')
        leave_room(room)
        session.clear()
        emit('status', {'msg': username + ' has left the room.'}, room=room)


    @socketio.on('join', namespace='/game')
    def join(message):
        room = "Main Hole"
        room = session.get('room')
        join_room(room)
        board = models.Board.query.filter_by()

        ln = 0
        for i in board:
            ln += 1
        print("ln: ", ln)
        ok = 1
        if ln == 0:
            state = None
            ok = 0
        else:
            state = board[ln-1].boardState
        emit('status', {'msg':  str(session.get('username')) + ' has entered the room.', 'board': state, 'ok': ok}, room=room)
    

    @socketio.on('newBoard', namespace='/game')
    def board(message):
        room = session.get('room')
        board = message['board']
        join_room(room)
        b = models.Board(boardState = message['board'])
        db.session.add(b)
        db.session.commit()
        emit('getBoard', {'board': board}, room=room)

    @socketio.on('money', namespace='/game')
    def board(message):
        room = session.get('room')
        username = session.get('username')
        amount = message['amount']
        join_room(room)
        user = models.User.query.filter_by(first_name = username).first()
        print(username)
        print(user.first_name)
        user.money = amount
        db.session.commit()
        emit('getMoney',{'money': amount, 'user': username}, room = room)
    
    socketio.run(app)

    