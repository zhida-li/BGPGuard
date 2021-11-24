#!/usr/bin/env python
from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, emit
from threading import Lock
import random

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bgp-ad-experiment')
def bgpexperiment():
    header1 = "Experiment"
    return render_template('bgp-ad-experiment.html', header1=header1)

@app.route('/bgp-ad-realtime')
def bgpadrealtime():
    header2 = "Real-time Detection"
    return render_template('bgp-ad-realtime.html', header2=header2)

# @app.route('/',methods=["POST"])
# def analyze():
#     model_choice = request.form['model_choice']
#     if request.method == 'POST':
#         if model_choice == 'ripe':
#             result_prediction = random.randint(1000, 1500)
#         elif model_choice == 'routeviews':
#             result_prediction = random.randint(1500, 2000)
#     return render_template('index.html',
#                                         result_prediction=result_prediction,
#                                         model_selected=model_choice)


@socketio.on('connect', namespace='/test_conn')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


def background_thread():
    while True:
        socketio.sleep(2)
        t1 = random.randint(1, 50)
        t2 = random.randint(50, 100)
        socketio.emit('server_response',
                      {'data': [t1, t2]}, namespace='/test_conn')


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True)
    
"""
use of app.run vs. socketio.run :

https://github.com/miguelgrinberg/Flask-SocketIO/issues/1273
Flask-SocketIO needs a web server. There are a few that you can use:
The Gevent web server, started via socketio.run()
The eventlet web server, also started via socketio.run()
The Flask dev web server, which can be started either via app.run() or for convenience also via socketio.run()
The Gunicorn web server with the eventlet or gevent workers, started via the gunicorn command.
The uwsgi web server with gevent, started via the uwsgi command.
"""    
    
