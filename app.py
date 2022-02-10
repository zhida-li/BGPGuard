# Author: Zhida Li
# last edit: Feb. 9, 2022
# task: offline function

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

sys.path.append('./apps/app_realtime/')
from dataDownload import data_downloader_single
from dataDownload import updateMessageName
from featureExtraction import feature_extractor_single
from time_locator import time_locator_single

sys.path.append('./apps/app_realtime/BLS_SFU_CNL_V101')
from BLS_SFU_CNL_V101.BLS_demo import bls_demo

# Flask configuration
async_mode, app, socketio, thread, thread_lock = flask_config()

# str titles
header_realTime = "Real-Time BGP Anomaly Detection"
header_offLine = "Off-Line BGP Anomaly Classification"


# Home index (route)
@app.route('/')
def index():
    return render_template('index.html')


# Real-Time Detection (route)
@app.route('/bgp_ad_realtime')
def bgp_ad_realtime():
    return render_template('bgp_ad_realtime.html', header1=header_realTime,
                           async_mode=socketio.async_mode)


# Off-Line Classification (route)
@app.route('/bgp_ad_offline')
def bgp_ad_offline():
    return render_template('bgp_ad_offline.html', header2=header_offLine)


# Received parameters for the off-Line experiment
@app.route('/bgp_ad_offline', methods=['POST'])
def analyze_offline():
    print('Dict. params. received from the front-end: \n', request.form)  # check if receive keys (name) from front-end
    model_params = {'site_choice',
                    'start_date_key', 'end_date_key',
                    'start_date_anomaly_key', 'end_date_anomaly_key',
                    'start_time_anomaly_key', 'end_time_anomaly_key',
                    'cut_pct_key',
                    'rnn_seq_key'}

    if model_params == set(request.form.keys()):
        print("Parameter received from the front-end.")
        site_choice = request.form.get('site_choice')  # or use 'request.form['']' due to dict format
        if site_choice == 'ripe':
            result_prediction = random.randint(100, 200)
        elif site_choice == 'routeviews':
            result_prediction = random.randint(200, 300)
        # store the var
        site_choice = 'RIPE' if site_choice == 'ripe' else 'Route Views'
        context_offLine = {"result_prediction": result_prediction,
                           "site_selected": site_choice,
                           "header2": header_offLine}
        time.sleep(5)
        return render_template('bgp_ad_offline.html', **context_offLine)
        # return render_template('bgp_ad_offline.html', result_prediction=result_prediction)
    else:
        return render_template('bgp_ad_offline.html', header2=header_offLine)


# Contact (route)
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Websocket for Real-Time Detection  -begin
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
    time_interval = 5 * 60  # RIPE provides new update msg every 5 minutes

    while True:
        # if second = 5, wait 1 min until RIPE or Route Views do update
        if int(time.strftime('%M', time.localtime())) % 5 == 0:
            time.sleep(60)

        # start processing...
        time_start = time.time()

        year, month, day, hour, minute = time_locator_single(site)
        update_message_file, data_date = updateMessageName(year, month, day, hour, minute)
        print("=> >>>>>>>>>> > > > > > ",
              "Processing update_message_file:", update_message_file,
              " < < < < < <<<<<<<<<< <= \n")
        data_downloader_single(update_message_file, data_date, site)
        file_name = feature_extractor_single(site)  # file_name not use

        if ALGOs == 'BLS':
            # BLS
            predicted_labels, test_hour_chart, test_min_chart, web_results = bls_demo()
            # print("predicted", predicted_labels)  # type: [2.0, 1.0, ...]
            # print("test_hour", test_hour_chart)  # type: ['01', '01', ...]
            # print("web_results", web_results)
        elif ALGOs == 'GRU':
            # GRU
            # gru2_demo()
            print("Please re-enter.")
            exit()

        results_text1, results_text2, results_text3, results_text4, results_text5 \
            = web_results[0], web_results[1], web_results[2], web_results[3], web_results[4]

        t_utc = time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime())

        # Emit uct date & time, predicted labels of 5min
        socketio.emit('server_response_text',
                      {'data_results': [results_text1, results_text2, results_text3, results_text4, results_text5],
                       'data_t': [t_utc]}, namespace='/test_conn')
        socketio.sleep(0.5)

        # Prepare uct time, features
        t_ann = []  # t_ann = ['01:45', '01:46', ...]
        for i in range(len(test_hour_chart)):
            t_ann.append(test_hour_chart[i] + ':' + test_min_chart[i])

        path_app = 'apps/app_realtime/'
        data_for_plot = np.loadtxt('./%sdata_test/DUMP_out.txt' % path_app)
        data_for_plot_ann = data_for_plot[:, 4]
        data_for_plot_ann = data_for_plot_ann.tolist()
        data_for_plot_wd = data_for_plot[:, 5]
        data_for_plot_wd = data_for_plot_wd.tolist()
        # print(t_ann)
        # print(data_for_plot_ann)

        # Emit features, uct time
        socketio.emit('server_response_echart2',
                      {'data_features': [t_ann, data_for_plot_ann, data_for_plot_wd], 'count': count},
                      namespace='/test_conn')

        # Emit labels, uct time
        for i in range(len(predicted_labels)):
            if predicted_labels[i] == 2:
                predicted_labels[i] = 0

        socketio.emit('server_response_echart0',
                      {'data_labels': [t_ann, predicted_labels]},
                      namespace='/test_conn')
        socketio.sleep(0.5)

        # Emit multi-core cpu usage, uct time
        count += 1
        t_cpu = time.strftime('%H:%M:%S', time.gmtime())
        cpus = psutil.cpu_percent(interval=None, percpu=True)  # percentages for each core, 10 elements
        t_cpu = 10 * [t_cpu]  # 10 time elements, element type is string.

        socketio.emit('server_response_echart_cpu',
                      {'data_cpu': [t_cpu, cpus], 'count': count},
                      namespace='/test_conn')

        # completed processing...
        time_end = time.time()

        time_realTime_backEnd = time_end - time_start
        print('Entire processing time: %.4f s' % time_realTime_backEnd, '\n',
              'Current time:', time.strftime('%H:%M:%S', time.localtime()))
        t_sleep = time_interval - time_realTime_backEnd
        if t_sleep <= 0:
            continue
        time.sleep(t_sleep)
# Websocket for Real-Time Detection  -end


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

# code for testing socketio using random generated integer numbers:
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
