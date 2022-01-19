# Author: Zhida Li
# last edit: Dec. 7, 2021
# task: add ann plot, emit results to the client

import sys
import random
import time
# import external libraries
import numpy as np
from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock

import psutil

# import customized library
from config import flask_config

sys.path.append('/Users/zhidali/githubProject/BGPDetect-web-app/apps/app_realtime/')
from dataDownload import data_downloader_single
from dataDownload import updateMessageName
from featureExtraction import feature_extractor_single
from time_locator import time_locator_single

sys.path.append('/Users/zhidali/githubProject/BGPDetect-web-app/apps/app_realtime/BLS_SFU_CNL_V101')
from BLS_SFU_CNL_V101.BLS_demo import bls_demo

# Flask configuration
async_mode, app, socketio, thread, thread_lock = flask_config()


# Home
@app.route('/')
def index():
    return render_template('index.html')


# Real-Time Detection
@app.route('/bgp_ad_realtime')
def bgp_ad_realtime():
    header1 = "Real-Time Detection"
    return render_template('bgp_ad_realtime.html', header1=header1,
                           async_mode=socketio.async_mode)


# Off-Line Classification
@app.route('/bgp_ad_offline')
def bgp_ad_offline():
    header2 = "Off-Line Classification"
    return render_template('bgp_ad_offline.html', header2=header2)


# Contact
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Received parameters for the off-Line experiment
@app.route('/bgp_ad_offline', methods=["POST"])
def analyze_offline():
    header2 = "Off-Line Classification"
    model_choice = request.form['model_choice']
    if request.method == 'POST':
        if model_choice == 'ripe':
            result_prediction = random.randint(100, 200)
        elif model_choice == 'routeviews':
            result_prediction = random.randint(200, 300)
    return render_template('bgp_ad_offline.html',
                           result_prediction=result_prediction,
                           model_selected=model_choice, header2=header2)


@socketio.on('main_event', namespace='/test_conn')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread_cpu)


def background_thread_cpu():
    count = 0
    ALGOs = 'BLS'
    site = 'RIPE'
    time_interval = 330  # 5*60 add 30 sec because there is delay for ripe and routeviews.

    while True:
        year, month, day, hour, minute = time_locator_single(site)
        update_message_file, data_date = updateMessageName(year, month, day, hour, minute)
        print('=> >>>>>>>>>> > > > > > ',
              'Processing update_message_file:', update_message_file,
              ' < < < < < <<<<<<<<<< <= \n')
        data_downloader_single(update_message_file, data_date, site)
        file_name = feature_extractor_single(site)  # file_name not use

        if ALGOs == 'BLS':
            # BLS
            predicted_list, test_hour, test_min, web_results = bls_demo()
            predicted_list, test_hour_list, test_min_list = predicted_list, test_hour.tolist(), test_min.tolist()
            # print("predicted", predicted_list)
            # print("test_hour", test_hour_list)
            # print("test_min", test_min_list)
            # print("web_results", web_results)
        elif ALGOs == 'GRU':
            # GRU
            # gru2_demo()
            print("Please re-enter.")
            exit()

        results_text1, results_text2, results_text3, results_text4, results_text5 \
            = web_results[0], web_results[1], web_results[2], web_results[3], web_results[4]

        t = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())  # time.localtime())
        # t2 = random.randint(1, 100)
        socketio.emit('server_response_text',
                      {'data': [t, results_text1, results_text2, results_text3, results_text4, results_text5]
                       }, namespace='/test_conn')

        socketio.sleep(1)
        t_ann = []
        for i in range(len(test_hour_list)):
            t_ann.append(str(int(test_hour_list[i])) + ':' + str(int(test_min_list[i])))

        path_app = "apps/app_realtime/"
        data_for_plot = np.loadtxt('./%sdata_test/DUMP_out.txt' % path_app)
        data_for_plot_ann = data_for_plot[:, 4]
        data_for_plot_ann = data_for_plot_ann.tolist()
        # print(t_ann)
        # print(data_for_plot_ann)

        socketio.emit('server_response_echart2',
                      {'data_cpu': [t_ann, data_for_plot_ann], 'count': count},
                      namespace='/test_conn')

        socketio.sleep(1)
        count += 1
        t_chart = time.strftime('%H:%M:%S', time.localtime())
        cpus = psutil.cpu_percent(interval=None, percpu=True)  # percentages for each core, 10 elements
        t_chart = 10 * [t_chart]  # 10 time elements, element type is string.

        socketio.emit('server_response_echart_cpu',
                      {'data_cpu': [t_chart, cpus], 'count': count},
                      namespace='/test_conn')
        time.sleep(time_interval)


# @socketio.on('main_event', namespace='/test_conn')
# def test_connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(target=background_thread_cpu)
#
#
# def background_thread_cpu():
#     count = 0
#     while True:
#         # socketio.sleep(2)
#         t = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
#         t2 = random.randint(1, 100)
#         socketio.emit('server_response',
#                       {'data': [t, t2]}, namespace='/test_conn')
#
#         socketio.sleep(1)
#         count += 1
#         t_chart = time.strftime('%H:%M:%S', time.localtime())
#         cpus = psutil.cpu_percent(interval=None, percpu=True)  # percentages for each core, 10 elements
#         t_chart = 10 * [t_chart]  # 10 time elements
#         # cpus = sum(cpus)/len(cpus) # avg cpu %
#         # generate 3 arrays, announcement, results vs. time.
#         socketio.emit('server_response_echart',
#                       {'data_cpu': [t_chart, cpus], 'count': count},
#                       namespace='/test_conn')

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
