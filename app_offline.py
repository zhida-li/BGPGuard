"""
    @author Zhida Li
    @email zhidal@sfu.ca
    @date Feb. 19, 2022
    @version: 1.1.0
    @description:
                This module contains the function for off-line classification.
                It used for HTTP 'POST' method for the front-end.

    @copyright Copyright (c) Feb. 19, 2022
        All Rights Reserved

    This Python code (versions 3.6 and newer)
"""

# ==============================================
# bgpGuard off-line module
# ==============================================
# Last modified: Feb. 19, 2022

# Import the built-in libraries
import time
import random

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


def app_offline_classification(header_offLine, site_choice):
    """
    :param header_offLine: header for off-line route
    :param site_choice: collection site
    :return: data for render_template (POST method)
    """
    if site_choice == 'ripe':
        result_prediction = random.randint(100, 200)
    elif site_choice == 'routeviews':
        result_prediction = random.randint(200, 300)
    # store the var
    site_choice = 'RIPE' if site_choice == 'ripe' else 'Route Views'
    context_offLine = {"result_prediction": result_prediction,
                       "site_selected": site_choice,
                       "header2": header_offLine}
    return context_offLine


"""
Data format received from the front-end:

ImmutableMultiDict([('site_choice', 'ripe'), ('start_date_key', '20050523'), ('end_date_key', '20050527'), 
('start_date_anomaly_key', '20050525'), ('end_date_anomaly_key', '20050525'), 
('start_time_anomaly_key', '0400'), ('end_time_anomaly_key', '1159'), ('cut_pct_key', '82'), ('rnn_seq_key', '10')])
"""
