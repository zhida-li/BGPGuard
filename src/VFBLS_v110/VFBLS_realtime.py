"""
    @author Zhida Li
    @email zhidal@sfu.ca
    @date Feb. 19, 2022
    @version: 1.1.0
    @description:
                This module contains the vfbls function
                for loading data and prediction.

    @copyright Copyright (c) Feb. 19, 2022
        All Rights Reserved

    This Python code (versions 3.6 and newer)
"""

# ==============================================
# VFBLS real-time detection high-level module
# ==============================================
# Last modified: Feb. 27, 2022

# Import the built-in libraries
import os
import sys
import time
import random

# Import external libraries
import numpy as np
from scipy.stats import zscore

# Import customized libraries
sys.path.append('./src/VFBLS_v110')
from bls.processing.replaceNan import replaceNan
from bls.model.bls_train_realtime import bls_train_fscore_online
from bls.model.vfbls_train import vfbls_train_realtime
from bls.model.vfbls_test import vfbls_test_realtime


# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)


# ====== For training/testing ======
def vfbls_demo_train_test():
    # Disable
    def blockPrint():
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def enablePrint():
        sys.stdout = sys.__stdout__

    blockPrint()

    # Load the datasets
    path_app = "src"
    train_dataset0 = np.loadtxt("./%s/data_historical/Code_Red_I.csv" % path_app, delimiter=",")
    train_dataset1 = np.loadtxt("./%s/data_historical/Nimda.csv" % path_app, delimiter=",")
    train_dataset2 = np.loadtxt("./%s/data_historical/Slammer.csv" % path_app, delimiter=",")
    train_dataset3 = np.loadtxt("./%s/data_historical/Moscow_blackout.csv" % path_app, delimiter=",")
    train_dataset4 = np.loadtxt("./%s/data_historical/WannaCrypt.csv" % path_app, delimiter=",")
    train_dataset5 = np.loadtxt("./%s/data_historical/RIPE_regular.csv" % path_app, delimiter=",")
    train_dataset6 = np.loadtxt("./%s/data_historical/BCNET_regular.csv" % path_app, delimiter=",")

    test_dataset = np.loadtxt('./%s/data_test/DUMP_out.txt' % path_app)
    # np.savetxt('./test_dataset.csv', test_dataset, delimiter=',',fmt='%.8f')

    # Combine training data
    train_dataset_list = [train_dataset1, train_dataset2, train_dataset3,
                          train_dataset4, train_dataset5, train_dataset6]
    train_dataset = train_dataset0
    for train_data in train_dataset_list:
        train_dataset = np.concatenate((train_dataset, train_data), axis=0)
    # np.savetxt('./train_dataset.csv', train_dataset, delimiter=',', fmt='%.4f')

    row_index_end = train_dataset.shape[0] - train_dataset.shape[0] % 100  # divisible by 100
    train_x = train_dataset[:row_index_end, 4:-1]
    train_x = zscore(train_x, axis=0, ddof=1)  # For each feature, mean = 0 and std = 1
    replaceNan(train_x)  # Replace "nan" with 0
    train_y = train_dataset[:row_index_end, -1]

    # Change training labels
    inds1 = np.where(train_y == -1)
    train_y[inds1] = 2

    # new process test data #
    test_x = test_dataset[:, 4:]

    # Normalize test data
    test_x = zscore(test_x, axis=0, ddof=1)  # For each feature, mean = 0 and std = 1
    replaceNan(test_x)  # Replace "nan" with 0
    # test_y = test_dataset[:, -1];

    # # Change test labels
    # inds2 = np.where(test_y == 0);
    # test_y[inds2] = 2;

    # VFBLS parameters
    seed = 1  # set the seed for generating random numbers
    num_class = 2  # number of the classes
    epochs = 1  # number of epochs

    C = 2 ** -15  # parameter for sparse regularization
    s = 0.6  # the shrinkage parameter for enhancement nodes

    #######################
    # N1* - the number of mapped feature nodes
    # N2* - the groups of mapped features
    # N3* - the number of enhancement nodes

    N1_bls_fsm = 100
    N2_bls_fsm = 10
    N3_bls_fsm = 100

    N1_bls_fsm1 = 30
    N2_bls_fsm1 = 10

    N1_bls_fsm2 = 30
    N2_bls_fsm2 = 10

    add_nFeature1 = 16
    add_nFeature2 = 8
    #######################

    train_err = np.zeros((1, epochs))
    train_time = np.zeros((1, epochs))
    test_time = np.zeros((1, epochs))

    # VFBLS ----------------------------------------------------------------
    print("======================= VFBLS =======================\n")
    np.random.seed(seed)  # set the seed for generating random numbers
    for j in range(0, epochs):
        trainingAccuracy, trainingTime, testingTime, predicted \
            = vfbls_train_realtime(train_x, train_y, test_x,
                                   s, C,
                                   N1_bls_fsm, N2_bls_fsm, N3_bls_fsm,
                                   N1_bls_fsm1, N2_bls_fsm1, N1_bls_fsm2, N2_bls_fsm2,
                                   add_nFeature1, add_nFeature2)

        train_err[0, j] = trainingAccuracy * 100
        train_time[0, j] = trainingTime
        test_time[0, j] = testingTime

    # print("======================= BLS =======================\n")
    # np.random.seed(seed)  # set the seed for generating random numbers
    # for j in range(0, epochs):
    #     TrainingAccuracy, Training_time, Testing_time, predicted = \
    #         bls_train_fscore_online(train_x, train_y, test_x, s, C, N1_bls, N2_bls, N3_bls)
    #
    #     train_err[0, j] = trainingAccuracy * 100
    #     train_time[0, j] = trainingTime
    #     test_time[0, j] = testingTime

    enablePrint()
    # print("trn acc:", trainingAccuracy)

    # predicted = [[1.], [2.], [2.], [2.], [2.]]
    predicted_list = []
    for label in predicted:
        predicted_list.append(label[0])

    # string to the front-end
    web_results = []
    test_hour_chart = []
    test_min_chart = []
    test_hour, test_min = test_dataset[:, 1], test_dataset[:, 2]
    for label, hour, minute in zip(predicted, test_hour, test_min):
        hour, minute = int(hour), int(minute)
        hour = str(hour)
        if len(hour) == 1:
            hour = '0' + hour
        minute = str(minute)
        if len(minute) == 1:
            minute = '0' + minute
        if label == 1:
            print("\n Detection time (HH:MM) %s : %s => An anomaly is detected!" % (hour, minute))
            web_results.append("Detection time (HH:MM) %s : %s => An anomaly is detected!" % (hour, minute))
        else:
            print("\n Detection time (HH:MM) %s : %s => Normal traffic" % (hour, minute))
            web_results.append("Detection time (HH:MM) %s : %s => Normal traffic" % (hour, minute))
        test_hour_chart.append(hour)
        test_min_chart.append(minute)
    return predicted_list, test_hour_chart, test_min_chart, web_results


# ====== For testing only ======
def vfbls_demo(mem='low'):
    # Disable
    def blockPrint():
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def enablePrint():
        sys.stdout = sys.__stdout__

    blockPrint()

    # Load the datasets
    path_app = "src"
    test_dataset = np.loadtxt('./%s/data_test/DUMP_out.txt' % path_app)

    # new process test data #
    test_x = test_dataset[:, 4:]

    # Normalize test data
    test_x = zscore(test_x, axis=0, ddof=1)  # For each feature, mean = 0 and std = 1
    replaceNan(test_x)  # Replace "nan" with 0

    # VFBLS parameters
    seed = 1  # set the seed for generating random numbers
    num_class = 2  # number of the classes
    epochs = 1  # number of epochs

    # C = 2 ** -15  # parameter for sparse regularization
    # s = 0.6  # the shrinkage parameter for enhancement nodes

    #######################
    # N1* - the number of mapped feature nodes
    # N2* - the groups of mapped features
    # N3* - the number of enhancement nodes

    # high:
    # N1_bls_fsm = 100
    # N2_bls_fsm = 10
    # N3_bls_fsm = 100
    #
    # N1_bls_fsm1 = 30
    # N2_bls_fsm1 = 10
    #
    # N1_bls_fsm2 = 30
    # N2_bls_fsm2 = 10
    #
    # add_nFeature1 = 16
    # add_nFeature2 = 8

    # low:
    # N1_bls_fsm = 20
    # N2_bls_fsm = 5
    # N3_bls_fsm = 10
    #
    # N1_bls_fsm1 = 10
    # N2_bls_fsm1 = 5
    #
    # N1_bls_fsm2 = 10
    # N2_bls_fsm2 = 5
    #
    # add_nFeature1 = 16
    # add_nFeature2 = 8
    #######################

    # train_err = np.zeros((1, epochs))
    # train_time = np.zeros((1, epochs))
    test_time = np.zeros((1, epochs))

    # VFBLS ----------------------------------------------------------------
    print("======================= VFBLS =======================\n")
    np.random.seed(seed)  # set the seed for generating random numbers
    for j in range(0, epochs):
        _, _, testingTime, predicted \
            = vfbls_test_realtime(test_x, mem)

        # train_err[0, j] = trainingAccuracy * 100
        # train_time[0, j] = trainingTime
        test_time[0, j] = testingTime

    enablePrint()
    # print("mem:", mem)

    # predicted = [[1.], [2.], [2.], [2.], [2.]]
    predicted_list = []
    for label in predicted:
        predicted_list.append(label[0])

    # string to the front-end
    web_results = []
    test_hour_chart = []
    test_min_chart = []
    test_hour, test_min = test_dataset[:, 1], test_dataset[:, 2]
    for label, hour, minute in zip(predicted, test_hour, test_min):
        hour, minute = int(hour), int(minute)
        hour = str(hour)
        if len(hour) == 1:
            hour = '0' + hour
        minute = str(minute)
        if len(minute) == 1:
            minute = '0' + minute
        if label == 1:
            print("\n Detection time (HH:MM) %s : %s => An anomaly is detected!" % (hour, minute))
            web_results.append("Detection time (HH:MM) %s : %s => An anomaly is detected!" % (hour, minute))
        else:
            print("\n Detection time (HH:MM) %s : %s => Normal traffic" % (hour, minute))
            web_results.append("Detection time (HH:MM) %s : %s => Normal traffic" % (hour, minute))
        test_hour_chart.append(hour)
        test_min_chart.append(minute)
    return predicted_list, test_hour_chart, test_min_chart, web_results
