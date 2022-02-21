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
# Last modified: Feb. 20, 2022

# Import the built-in libraries
import os

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


def flask_folder():
    dataSplit_folder = './src/data_split'
    dataTest_folder = './src/data_test'
    parmSel_folder = './src/parmSel'
    STAT_folder = './src/STAT'
    temp_ripe_folder = './src/data_ripe/temp'
    temp_routeviews_folder = './src/data_routeviews/temp'

    if not os.path.exists(dataSplit_folder):
        os.makedirs(dataSplit_folder)
    if not os.path.exists(dataTest_folder):
        os.makedirs(dataTest_folder)
    if not os.path.exists(parmSel_folder):
        os.makedirs(parmSel_folder)
    if not os.path.exists(STAT_folder):
        os.makedirs(STAT_folder)
    if not os.path.exists(temp_ripe_folder):
        os.makedirs(temp_ripe_folder)
    if not os.path.exists(temp_routeviews_folder):
        os.makedirs(temp_routeviews_folder)

        print("\n BGPGuard => >>>>>>>>>> Folders have been created.")
    return None
