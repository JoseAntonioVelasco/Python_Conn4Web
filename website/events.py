from flask import session
from flask_socketio import emit, join_room, leave_room
from flask import Blueprint
from . import socketio

events = Blueprint('events',__name__)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received something: '+str(json))
    join_room(66)
    socketio.emit('my response', json, room=66)

@socketio.on('join')
def join(message, namespace='/match'):
    print('ha entrado al join')
    matchID = int(session.get('room'))
    print(matchID)
    join_room(matchID)
    emit('status', {'msg': session.get('username') + ' ha entrado a la sala'}, room = matchID)
