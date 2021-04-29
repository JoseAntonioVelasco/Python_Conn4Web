from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
from .models import Match, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/match', methods=['GET', 'POST'])
@login_required
def createMatch():
    if request.method == 'GET':
        # genera una nueva partida
        new_match = Match(user1_id=current_user.id,
                          status="Waiting", turn=current_user.id, solo=False)
        db.session.add(new_match)
        db.session.commit()

        session['username'] = current_user.first_name
        session['room'] = new_match.id

        return render_template("match.html", user=current_user, session=session)

    elif request.method == 'POST':
        # buscar id de partida
        matchId = request.form.get('matchId')

        if len(matchId) < 1:
            flash('No has introducido un id!', category='error')
            return redirect(url_for('views.joinMatch'))

        else:
            match = Match.query.get(matchId)
            if match == None:
                # ese id de partida no existe
                flash('No existe esa partida!', category='error')
                return redirect(url_for('views.joinMatch'))

            elif match.status == "Finished":
                # partida ya acabada
                flash('Esa partida ya ha acabado!', category='error')
                return redirect(url_for('views.joinMatch'))

            elif match.user1_id != current_user.id and match.user2_id == None:
                # se une a una partida que estaba esperando
                # cambiamos el estado de la partida a Started
                match.status = "Started"
                match.user2_id = current_user.id
                db.session.commit()

                session['username'] = current_user.first_name
                session['room'] = matchId

                return render_template('match.html', user=current_user, session=session)

            elif match.user1_id != current_user.id and match.user2_id != current_user.id:
                # Este jugador no pertenece a esta partida
                flash('Esta partida ya esta llena!', category='error')
                return redirect(url_for('views.joinMatch'))
            else:
                # ese id de partida existe
                session['username'] = current_user.first_name
                session['room'] = matchId

                return render_template('match.html', user=current_user, session=session)


@views.route('/joinMatch', methods=['GET', 'POST'])
@login_required
def joinMatch():
    return render_template('joinMatch.html', user=current_user)
