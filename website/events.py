from flask import session, Blueprint, flash
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from sqlalchemy.sql import func
from . import socketio, db
from .con4 import utilities as u
from .models import getBoard, getMatchInfo, Move, Match, User

events = Blueprint('events', __name__)


@socketio.on('join')
def join(message, namespace='/match'):
    # conseguimos el matchID al que ha entrado y le unimos al socket
    matchID = int(session.get('room'))
    join_room(matchID)

    # le asignamos un color al usuario, si es el que crea la partida sera el color rojo, si es el que se une sera el amarillo
    match = Match.query.get(matchID)
    color = "undefined"
    if current_user.id == match.user1_id:
        color = "red"
    else:
        color = "yellow"

    # conseguimos el tablero de esa partida
    board = getBoard(matchID)
    matchInfo = getMatchInfo(matchID)
    emit('status', {'msg': session.get('username') + ' ha entrado a la sala',
                    'board': board, 'matchInfo': matchInfo, 'color': color}, room=matchID)


@socketio.on('text')
def text(message, namespace='/match'):
    matchID = int(session.get('room'))
    emit('message', {'msg': session.get('username') +
                     ' : ' + message['msg']}, room=matchID)


@socketio.on('place')
def place(data, namespace='/match'):
    matchID = int(session.get('room'))

    x = int(data['x'])
    y = int(data['y'])
    color = data['color']

    match = Match.query.get(matchID)
    # si todavia no ha entrado un rival no puede mover
    if match.status == "Waiting":
        emit('notice', {
             'msg': 'La partida esta esperando a un jugador'}, room=matchID)
        return
    elif match.status == "Finished":
        emit('notice', {'msg': 'La partida ha acabado!'}, room=matchID)
        return
    # para que pueda mover tiene que ser su turno
    elif current_user.id == match.turn or match.solo:
        # conseguimos el numero de turno para saber si es empate
        nturn = db.session.query(func.count(Move.id_match)).filter(
            Move.id_match == matchID).one()
        turn_number = nturn[0]
        # comprueba si el movimiento es valido
        board = getBoard(matchID)
        if u.legalMove(board, x, y) == False:
            # movimiento no valido
            return
        # comprueba si el movimiento es ganador o empate
        elif u.win(board, x, y, color) or turn_number == 41:
            match.status = "Finished"
        # añadimos el movimiento a la base de datos
        new_move = Move(id_match=matchID, x=x, y=y,
                        color=color, nturn=turn_number)
        db.session.add(new_move)
        # rota turno
        if match.turn == match.user1_id:
            match.turn = match.user2_id
        else:
            match.turn = match.user1_id
        db.session.commit()
        emit('place', {'x': x, 'y': y, 'color': color}, room=matchID)
    else:
        # no es su turno
        return


@socketio.on('aiJoin')
def aiJoin(data, namespace='/match'):
    matchID = int(session.get('room'))
    match = Match.query.get(matchID)

    if match.user2_id:
        # ya hay un jugador en la partida
        return

    # sacamos el usuario de la ia
    ai_id = int(data['ai'])
    ai_user = User.query.get(ai_id)

    # se elige en que orden empieza la partida
    if data['color'] == 'red':
        match.user1_id = ai_id
        match.turn = ai_id
        match.user2_id = current_user.id
    else:
        match.user2_id = ai_id

    # empieza la partida y guardamos los datos
    match.status = "Started"
    match.solo = True
    db.session.commit()

    matchInfo = getMatchInfo(matchID)
    emit('status', {'msg': 'La IA: ' + ai_user.first_name +
                    ' ha entrado a la sala', 'matchInfo': matchInfo}, room=matchID)
