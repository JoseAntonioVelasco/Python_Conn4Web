from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #sacamos los datos del formulario
        email = request.form.get('email')
        password = request.form.get('password')
        
        #si el email del usuario existe
        user = User.query.filter_by(email=email).first()
        if user:
            #comprueba que los hashes de la contraseña coinciden
            if check_password_hash(user.password, password):
                flash('Has iniciado sesión con éxito!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Contraseña incorrecta, prueba de nuevo.', category='error')
        else:
            flash('No existe ese email.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        #sacamos los datos del formulario
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        
        user = User.query.filter_by(email=email).first()
        if user:
            #si el email ya existe no se puede registrar con ese email
            flash('Ya existe una cuenta con ese email.', category='error')
        elif len(email) < 4:
            #el email tiene que ser mas largo
            flash('El email tiene que ser mas largo de 3 caracteres.', category='error')
        elif len(first_name) < 2:
            #el nombre tiene que ser mas largo
            flash('El nombre tiene que ser mas largo que 1 caracter.', category='error')
        elif password1 != password2:
            #las contraseñas tienen que coincider
            flash('Las contraseñas no coinciden.', category='error')
        elif len(password1) < 7:
            #la contraseña debe tener al menos 7 caracteres
            flash('La contraseña debe de tener al menos 7 caracteres.', category='error')
        else:
            #si todas las condiciones han pasado crear un nuevo usuario
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            #despues de crear un nuevo usuario se loguea automaticamente
            login_user(new_user, remember=True)
            flash('Cuenta creada!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
