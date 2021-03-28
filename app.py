from website import create_app, socketio
app = create_app()
#ejecuta este fichero para iniciar la aplicacion

if __name__ == '__main__':
    socketio.run(app,debug=True)