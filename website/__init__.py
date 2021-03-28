from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_session import Session

db = SQLAlchemy()

DB_NAME = "database.db"

socketio = SocketIO(manage_session=False)
session = Session()

def create_app():
    app = Flask(__name__)
    #configuracion de la app

    #cifrar las cookies con una frase aleatoria
    app.config['SECRET_KEY'] = 'frase aleatoria'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SESSION_TYPE'] = 'filesystem'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .events import events

    #se añaden los blueprints a la app para que los pueda utilizar
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(events, url_prefix='/')

    from .models import User

    #crear base de datos
    create_database(app)

    #configuracion del login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Inicia sesión para poder acceder a la página."
    login_manager.init_app(app)

    #inicializamos estos objetos con la app
    socketio.init_app(app)
    session.init_app(app)

    #cargador de usuarios para el login_manager
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    #si no existe la base de datos la crea
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')