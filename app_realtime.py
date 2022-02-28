"""
    @author Zhida Li
    @email zhidal@sfu.ca
    @date Feb. 19, 2022
    @version: 1.1.0
    @description:
                This module contains the function for real-time detection.
                It operates the background thread.

    @copyright Copyright (c) Feb. 19, 2022
        All Rights Reserved

    This Python code (versions 3.6 and newer)
"""

# ==============================================
# bgpGuard real-time module
# ==============================================
# Last modified: Feb. 19, 2022

# Import the built-in libraries
import time

# Import external libraries
import numpy as np
import psutil
from flask_socketio import SocketIO, emit, disconnect

# Import customized libraries
# sys.path.append('./src')
from src.dataDownload import updateMessageName
from src.dataDownload import data_downloader_single
from src.featureExtraction import feature_extractor_single
from src.time_tracker import time_tracker_single

# sys.path.append('./src/VFBLS_v110')
from src.VFBLS_v110.VFBLS_realtime import vfbls_demo


def app_realtime_detection(ALGO='VFBLS', site='RIPE', count=0):
    """
    :param ALGO: algorithm
    :param site:  collection site
    :param count: no. of the real-time detection
    :return: data for socket.io
    """
    year, month, day, hour, minute = time_tracker_single(site)
    update_message_file, data_date = updateMessageName(year, month, day, hour, minute)
    print("=> >>>>>>>>>> > > > > > ",
          "Processing an update message file:", update_message_file,
          " < < < < < <<<<<<<<<< <= \n")
    data_downloader_single(update_message_file, data_date, site)
    file_name = feature_extractor_single(site)  # file_name not use

    # Prepare uct date & time, predicted labels of 5min
    if ALGO == 'VFBLS':
        # VFBLS
        predicted_labels, test_hour_chart, test_min_chart, web_results = vfbls_demo(mem='low')
        # print("predicted", predicted_labels)  # type: [2.0, 1.0, ...]
        # print("test_hour", test_hour_chart)  # type: ['01', '01', ...]
        # print("web_results", web_results)
    elif ALGO == 'GRU':
        # GRU
        # gru2_demo()
        print("Please re-enter.")
        exit()

    t_utc = time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime())

    # Prepare uct time, features
    t_ann = []  # t_ann = ['01:45', '01:46', ...]
    for i in range(len(test_hour_chart)):
        t_ann.append(test_hour_chart[i] + ':' + test_min_chart[i])

    path_app = 'src/'
    data_for_plot = np.loadtxt('./%sdata_test/DUMP_out.txt' % path_app)
    data_for_plot_ann = data_for_plot[:, 4]
    data_for_plot_ann = data_for_plot_ann.tolist()
    data_for_plot_wdrl = data_for_plot[:, 5]
    data_for_plot_wdrl = data_for_plot_wdrl.tolist()
    # print(t_ann)
    # print(data_for_plot_ann)

    # Prepare labels, uct time
    for i in range(len(predicted_labels)):
        if predicted_labels[i] == 2:
            predicted_labels[i] = 0

    # Prepare multi-core cpu usage, uct time
    count += 1
    t_cpu = time.strftime('%H:%M:%S', time.gmtime())
    cpus = psutil.cpu_percent(interval=None, percpu=True)  # percentages for each core, 10 elements
    cpus_avg = round(sum(cpus) / len(cpus), 2)  # %.2f
    cpus_avg = [cpus_avg]
    t_cpu = 1 * [t_cpu]  # element type: string

    return web_results, t_utc, t_ann, data_for_plot_ann, data_for_plot_wdrl, count, predicted_labels, t_cpu, cpus_avg


"""
ripe: 
https://data.ris.ripe.net/rrc04/
routeviews:
https://archive.routeviews.org/bgpdata/
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
