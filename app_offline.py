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
# Last modified: June 24, 2022

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
from src.dataDownload import data_downloader_multi
from src.featureExtraction import feature_extractor_single
from src.featureExtraction import feature_extractor_multi
from src.time_tracker import time_tracker_single
from src.label_generation import label_generator
from src.data_partition import data_partition
from src.data_process import normTrainTest
from src.subprocess_cmd import subprocess_cmd

# sys.path.append('./src/VFBLS_v110')
from src.VFBLS_v110.VFBLS_realtime import vfbls_demo


def app_offline_classification(header_offLine, input_exp_key):
    """
    :param header_offLine: header for off-line route
    :param input_exp_key:
    :return: data for render_template (POST method)
    """
    # Placeholder for test the transmission between font-end and back-end
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
    """

    # store the var
    # input_exp_key = [site, start_date, end_date, start_date_anomaly, end_date_anomaly, start_time_anomaly,
    #                  end_time_anomaly, cut_pct, rnn_seq]
    print(input_exp_key)
    site = input_exp_key[0]
    start_date, end_date = input_exp_key[1], input_exp_key[2]
    start_date_anomaly, end_date_anomaly = input_exp_key[3], input_exp_key[4]
    start_time_anomaly, end_time_anomaly = input_exp_key[5], input_exp_key[6]
    cut_pct = input_exp_key[7]
    rnn_seq = int(input_exp_key[8])
    print("--------------------Loading settings successfully-------------")

    collector_ripe = 'rrc04'
    data_downloader_multi(start_date, end_date, site, collector_ripe)
    output_file_list = feature_extractor_multi(start_date, end_date, site)
    # dataAdjustment(site, output_file_list)
    # output_file_list = ["DUMP_20030123_out.txt", "DUMP_20030124_out.txt", "DUMP_20030125_out.txt"]  # for debug
    labels = label_generator(start_date_anomaly, end_date_anomaly, start_time_anomaly, end_time_anomaly, site,
                             output_file_list)
    data_partition(cut_pct, site, output_file_list, labels, rnn_seq)
    # selected_features = feature_select_ExtraTrees(cut_pct, site, topFeatures=15)
    # print("Top features:", selected_features)
    normTrainTest(cut_pct, site)

    print("--------------------Experiment-Begin--------------------------")
    subprocess_cmd("cd src/; \
                    cp ./data_split/train_%s_%s_n.csv ./data_split/test_%s_%s_n.csv ./RNN_Running_Code/RNN_Run/dataset/ ; \
                    cd RNN_Running_Code/RNN_Run/dataset/; \
                    mv train_%s_%s_n.csv train.csv; mv test_%s_%s_n.csv test.csv; \
                    cd ..; cd ..; \
                    chmod +x integrate_run.sh; sh ./integrate_run.sh ; \
                    cd RNN_Run/; sh ./collect.sh; \
                    cp -r res_acc res_run ../data_representation/ ; \
                    cd .. ; cd data_representation/ ; \
                    python TableGenerator.py; " \
                   % (cut_pct, site, cut_pct, site, cut_pct, site, cut_pct, site))

    print("--------------------Experiment-end----------------------------")
    subprocess_cmd("cd src/; \
                    mv ./RNN_Running_Code/data_representation/data_representation_table.csv ./STAT/ ; \
    				mv ./STAT/data_representation_table.csv ./STAT/results_%s_%s.csv" \
                   % (cut_pct, site))

    # Remove generated folders
    subprocess_cmd("cd src/; \
                    cd RNN_Running_Code/RNN_Run/; \
                    rm -rf ./experiment/ ./res_acc/ ./res_run/ ./tmp/")

    # Information from back-end to front-end, "Results are available"
    context_offLine = {"result_prediction": input_exp_key,
                       "site_selected": "Results are ready to download!",
                       "header2": header_offLine}
    return context_offLine


"""
Data format received from the front-end:

ImmutableMultiDict([('site_choice', 'ripe'), ('start_date_key', '20050523'), ('end_date_key', '20050527'), 
('start_date_anomaly_key', '20050525'), ('end_date_anomaly_key', '20050525'), 
('start_time_anomaly_key', '0400'), ('end_time_anomaly_key', '1159'), ('cut_pct_key', '82'), ('rnn_seq_key', '10')])
"""
