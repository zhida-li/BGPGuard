"""
    @authors Zhida Li, Ana Laura Gonzalez Rios, and Guangyu Xu
    @email {zhidal, anag, gxa5}@sfu.ca
    @date Mar. 4, 2020
    @version: 1.0.1
    @description:
                This file creates BLS models based on a 'training_dataset' and 'test_dataset.'
                Each BLS model returns the performance results: accuracy, F-Score, and training time.

    @copyright Copyright (c) Sept. 14, 2019
        All Rights Reserved

    Python code (version 3.6)
"""

# ==============================================
# Main file
# Modules of the BLS, RBF-BLS, CFBLS, CEBLS, and CFEBLS
# algorithms
# ==============================================

# Import the built-in libraries
import os
import sys
import time
import random

# Import external libraries
import numpy as np
from scipy.stats import zscore

# Import customized libraries
sys.path.append('./src/BLS_SFU_CNL_V101')
from bls.processing.replaceNan import replaceNan
from bls.processing.one_hot_m import one_hot_m
from bls.model.bls_train_fscore_online import bls_train_fscore_online


# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)

def bls_demo():
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

    train_x = train_dataset[:, 0:train_dataset.shape[1] - 1];
    train_x = zscore(train_x, axis=0, ddof=1);  # For each feature, mean = 0 and std = 1
    replaceNan(train_x);  # Replace "nan" with 0
    train_y = train_dataset[:, train_dataset.shape[1] - 1: train_dataset.shape[1]];

    # Change training labels
    inds1 = np.where(train_y == 0);
    train_y[inds1] = 2;

    ## new process test data
    test_x = test_dataset[:, 4:];
    # print(test_x.shape)               # numpy
    # print(type(test_x))               # 5-by-37

    # Normalize test data
    test_x = zscore(test_x, axis=0, ddof=1);  # For each feature, mean = 0 and std = 1
    replaceNan(test_x);  # Replace "nan" with 0
    # test_y = test_dataset[:, test_dataset.shape[1]  - 1 : test_dataset.shape[1] ];

    # # Change test labels
    # inds1 = np.where(test_y == 0);
    # test_y[inds1] = 2;

    train_y = one_hot_m(train_y, num_class);
    # test_y = one_hot_m(test_y, num_class);

    # BLS parameters
    C = 2 ** -25;  # parameter for sparse regularization
    s = 0.8;  # the shrinkage parameter for enhancement nodes

    # N1* - the number of mapped feature nodes
    # N2* - the groups of mapped features
    # N3* - the number of enhancement nodes

    N1_bls = 30
    N2_bls = 20
    N3_bls = 20

    epochs = 1;  # number of epochs

    train_err = np.zeros((1, epochs));
    train_time = np.zeros((1, epochs));
    test_time = np.zeros((1, epochs));

    # # BLS ----------------------------------------------------------------
    print("================== BLS ===========================\n\n");

    np.random.seed(seed);  # set the seed for generating random numbers
    for j in range(0, epochs):
        TrainingAccuracy, Training_time, Testing_time, predicted = \
            bls_train_fscore_online(train_x, train_y, test_x, s, C, N1_bls, N2_bls, N3_bls);

        train_err[0, j] = TrainingAccuracy * 100;
        train_time[0, j] = Training_time;
        test_time[0, j] = Testing_time;

    bls_train_time = Training_time;
    bls_test_time = Testing_time;

    enablePrint()

    # print("ok: ", 'ok'), new
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
            print("\n Test time (HH:MM) %s : %s => An anomaly is detected!" % (hour, minute))
            web_results.append("Test time (HH:MM) %s : %s => An anomaly is detected!" % (hour, minute))
        else:
            print("\n Test time (HH:MM) %s : %s => Normal traffic" % (hour, minute))
            web_results.append("Test time (HH:MM) %s : %s => Normal traffic" % (hour, minute))
        test_hour_chart.append(hour)
        test_min_chart.append(minute)
    return predicted_list, test_hour_chart, test_min_chart, web_results

# bls_demo()
