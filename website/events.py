from flask import session
from flask_socketio import emit, join_room, leave_room
from flask import Blueprint
from . import socketio

events = Blueprint('events',__name__)



@socketio.on('join')
def join(message, namespace='/match'):
    print('ha entrado al join')
    matchID = int(session.get('room'))
    join_room(matchID)
    emit('status', {'msg': session.get('username') + ' ha entrado a la sala'}, room = matchID)

@socketio.on('text')
def text(message, namespace='/match'):
    print('ha entrado en text')
    matchID = int(session.get('room'))
    emit('message',{'msg': session.get('username') + ' : ' + message['msg']}, room = matchID)

@socketio.on('left')
def left(message, namespace='/match'):
    matchID = int(session.get('room'))
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status',{'msg: username' + 'ha salido de la sala'}, room = matchID)


#test event
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received something: '+str(json))
    join_room(66)
    socketio.emit('my response', json, room=66)