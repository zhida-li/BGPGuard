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
# Last modified: Feb. 22, 2022

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


# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)

def vfbls_demo():
    # Disable
    def blockPrint():
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def enablePrint():
        sys.stdout = sys.__stdout__

    blockPrint()
    seed = 1  # set the seed for generating random numbers
    num_class = 2  # number of the classes

    # Load the datasets
    path_app = "src/"
    train_dataset11 = np.loadtxt("./%sdata_historical/slammer_64_train_ripe.csv" % path_app, delimiter=",")
    train_dataset12 = np.loadtxt("./%sdata_historical/slammer_64_test_ripe.csv" % path_app, delimiter=",")

    train_dataset21 = np.loadtxt("./%sdata_historical/nimda_64_train.csv" % path_app, delimiter=",")
    train_dataset22 = np.loadtxt("./%sdata_historical/nimda_64_test.csv" % path_app, delimiter=",")

    train_dataset31 = np.loadtxt("./%sdata_historical/codered1_64_train.csv" % path_app, delimiter=",")
    train_dataset32 = np.loadtxt("./%sdata_historical/codered1_64_test.csv" % path_app, delimiter=",")

    train_dataset41 = np.loadtxt("./%sdata_historical/instance_matrix_test_ripe.csv" % path_app, delimiter=",")
    train_dataset42 = np.loadtxt("./%sdata_historical/instance_matrix_test_bcnet.csv" % path_app, delimiter=",")

    test_dataset = np.loadtxt('./%sdata_test/DUMP_out.txt' % path_app)
    # np.savetxt('./test_dataset.csv', test_dataset, delimiter=',',fmt='%.4f')

    # Normalize training data
    train_dataset1 = np.concatenate((train_dataset11, train_dataset12), axis=0)
    train_dataset2 = np.concatenate((train_dataset21, train_dataset22), axis=0)
    train_dataset3 = np.concatenate((train_dataset31, train_dataset32), axis=0)
    train_dataset4 = np.concatenate((train_dataset41, train_dataset42), axis=0)

    train_dataset = np.concatenate((train_dataset1, train_dataset2, train_dataset3, train_dataset4), axis=0)
    # np.savetxt('./train_dataset.csv', train_dataset, delimiter=',',fmt='%.4f')

    train_x = train_dataset[:, 0:train_dataset.shape[1] - 1]
    train_x = zscore(train_x, axis=0, ddof=1)  # For each feature, mean = 0 and std = 1
    replaceNan(train_x)  # Replace "nan" with 0
    train_y = train_dataset[:, -1]

    # Change training labels
    inds1 = np.where(train_y == 0)
    train_y[inds1] = 2

    # new process test data #
    test_x = test_dataset[:, 4:]

    # Normalize test data
    test_x = zscore(test_x, axis=0, ddof=1);  # For each feature, mean = 0 and std = 1
    replaceNan(test_x);  # Replace "nan" with 0
    # test_y = test_dataset[:, -1];

    # # Change test labels
    # inds2 = np.where(test_y == 0);
    # test_y[inds2] = 2;

    # BLS parameters
    C = 2 ** -10  # parameter for sparse regularization
    s = 0.8  # the shrinkage parameter for enhancement nodes

    # N1* - the number of mapped feature nodes
    # N2* - the groups of mapped features
    # N3* - the number of enhancement nodes

    #######################
    N1_bls_fsm = 30
    N2_bls_fsm = 10
    N3_bls_fsm = 100

    N1_bls_fsm1 = 20
    N2_bls_fsm1 = 10

    N1_bls_fsm2 = 20
    N2_bls_fsm2 = 10

    add_nFeature1 = 16
    add_nFeature2 = 8
    #######################

    epochs = 1  # number of epochs
    train_err = np.zeros((1, epochs))
    train_time = np.zeros((1, epochs))
    test_time = np.zeros((1, epochs))

    # VFBLS ----------------------------------------------------------------
    print("================== VFBLS ===========================\n\n")
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

    # np.random.seed(seed);  # set the seed for generating random numbers
    # for j in range(0, epochs):
    #     TrainingAccuracy, Training_time, Testing_time, predicted = \
    #         bls_train_fscore_online(train_x, train_y, test_x, s, C, N1_bls, N2_bls, N3_bls);
    #
    #     train_err[0, j] = trainingAccuracy * 100;
    #     train_time[0, j] = trainingTime;
    #     test_time[0, j] = testingTime;

    enablePrint()

    # predicted = [[1.], [2.], [2.], [2.], [2.]]
    predicted_list = []
    for label in predicted:
        predicted_list.append(label[0])

    # string to web
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
