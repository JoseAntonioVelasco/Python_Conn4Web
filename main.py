from website import create_app
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session

app = create_app()
socketio = SocketIO(app)

Session(app)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received something: '+str(json))
    socketio.emit('my response', json)

if __name__ == '__main__':
    socketio.run(app,debug=True)


