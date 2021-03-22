from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Match
from . import db
import json

views = Blueprint('views',__name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/match',methods=['GET','POST'])
@login_required
def createMatch():
    #generar un id de partida
    if request.method == 'GET':
        new_match = Match(user1_id=current_user.id, status="Waiting")
        db.session.add(new_match)
        db.session.commit()
    return render_template("match.html", user=current_user ,match=new_match)


@views.route('/joinMatch',methods=['GET','POST'])
@login_required
def joinMatch():
    #buscar id de partida
    if request.method == 'POST':
        matchId = request.form.get('matchId')

        if len(matchId) < 1:
            flash('No has introducido un id!', category='error')
        else:
            match = Match.query.get(matchId)
            if match == None:
                #ese id de partida no existe
                flash('No existe esa partida!', category='error')
            elif match.status == "Finished":
                #partida ya acabada
                flash('Esa partida ya ha acabado!', category='error')
            elif match.user1_id != current_user.id and match.user2_id == None:
                #se une a una partida que estaba esperando
                db.session.delete(match)
                match.status="Started"
                match.user2_id=current_user.id
                db.session.add(match)
                db.session.commit()
                return render_template('match.html', user=current_user, match=match)
            elif match.user1_id != current_user.id and match.user2_id != current_user.id:
                #Este jugador no pertenece a esta partida
                flash('Esta partida ya esta llena!', category='error')
            else:
                #ese id de partida existe
                return render_template('match.html', user=current_user, match=match)
    return render_template('joinMatch.html', user=current_user)

@views.route('/place', methods=['POST'])
def place():
    position = json.loads(request.data)

   
    
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})