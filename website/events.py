from flask import session, Blueprint, flash
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from sqlalchemy.sql import func
from . import socketio, db
from .con4 import utilities as u
from .models import getBoard, Move, Match

events = Blueprint('events',__name__)


@socketio.on('join')
def join(message, namespace='/match'):
    print('ha entrado al join')
    #conseguimos el matchID al que ha entrado y le unimos al socket
    matchID = int(session.get('room'))
    join_room(matchID)

    #le asignamos un color al usuario, si es el que crea la partida sera el color rojo, si es el que se uno sera el amarillo
    match = Match.query.get(matchID)
    color = "undefined"
    if current_user.id == match.user1_id:
        color = "red"
    else:
        color = "yellow"

    #conseguimos el tablero de esa partida
    board = getBoard(matchID)
    emit('status', {'msg': session.get('username') + ' ha entrado a la sala', 'board': board, 'color': color}, room = matchID)

@socketio.on('text')
def text(message, namespace='/match'):
    print('ha entrado en text')
    matchID = int(session.get('room'))
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room = matchID)

@socketio.on('left')
def left(message, namespace='/match'):
    matchID = int(session.get('room'))
    username = session.get('username')
    leave_room(matchID)
    session.clear()
    emit('status',{'msg: username' + 'ha salido de la sala'}, room = matchID)

@socketio.on('place')
def place(data, namespace='/match'):
    print('ha entrado al place')
    matchID = int(session.get('room'))
    print(data)
    
    x = int(data['x'])
    y = int(data['y'])
    color = data['color']
    
    match = Match.query.get(matchID)
    #si todavia no ha entrado un rival no puede mover
    if match.status == "Waiting" or match.status == "Finished":
        print('La partida esta waiting o a acabado')
        return
    #para que pueda mover tiene que ser su turno
    elif current_user.id == match.turn:
        #comprueba si el movimiento es valido
        board = getBoard(matchID)
        if u.legalMove(board, x, y) == False:
            print('Movimiento no valido, ¿haciendo trampas?')
            return
        #comrpueba si el movimiento es ganador
        elif u.win(board, x, y, color):
            match.status = "Finished"
            flash('Hay un ganador', category='success')
        #añadimos el movimiento a la base de datos
        nturn = db.session.query(func.count(Move.id_match)).filter(Move.id_match == matchID)
        new_move = Move(id_match=matchID, x=x, y=y, color=color, nturn=nturn)
        db.session.add(new_move)
        #rota turno
        if match.turn == match.user1_id:
            match.turn = match.user2_id
        else:
            match.turn = match.user1_id
        db.session.commit()

        emit('place', {'x': x, 'y':y, 'color':color}, room = matchID)
    else:
        print('no es tu turno')
    
