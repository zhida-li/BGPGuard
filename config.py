"""
    @author Zhida Li
    @email zhidal@sfu.ca
    @date Feb. 19, 2022
    @version: 1.1.0
    @description:
                Flask socket.io configuration.

    @copyright Copyright (c) Feb. 19, 2022
        All Rights Reserved

    This Python code (versions 3.6-3.8)
"""

# ==============================================
# Flask socket.io configuration
# ==============================================
# Last modified: Feb. 19, 2022

# Import the external libraries
from flask import Flask
from flask_socketio import SocketIO
from threading import Lock


def flask_config():
    async_mode = None
    # Declare a Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app, async_mode=async_mode)
    thread = None
    thread_lock = Lock()

    return async_mode, app, socketio, thread, thread_lock
