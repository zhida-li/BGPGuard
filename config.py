# flask socket.io configuration
from flask import Flask
from flask_socketio import SocketIO
from threading import Lock


def flask_config():
    async_mode = None
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app, async_mode=async_mode)
    thread = None
    thread_lock = Lock()

    return async_mode, app, socketio, thread, thread_lock
