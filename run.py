from api import createapp

def startApp(debug=False):
    app = createapp(debug)
    if not debug:
        app.run()
    else:
        from api import socketio
        socketio.run(app)
        
if __name__ == "__main__":
    startApp()