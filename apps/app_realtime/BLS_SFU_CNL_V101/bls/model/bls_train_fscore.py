"""
    @authors Zhida Li, Ana Laura Gonzalez Rios, and Guangyu Xu
    @email {zhidal, anag, gxa5}@sfu.ca
    @date Sept. 14, 2019
    @version: 1.0.0
    @description:
                This library contains the module of the BLS algorithm. It includes
                the function 'bls_train_fscore.'
                Function 'accuracy_score' is used to calculate the accuracy while 'f1_score'
                is used to get the F-Score.

    @copyright Copyright (c) Sept. 14, 2019
        All Rights Reserved

    This Python code (version 3.6) is translated from MATLAB code (version 2017b)
    (http://www.broadlearning.ai/).
"""

######################################################
####### BLS 
######################################################

# Import the Python libraries
import time
import random
import numpy as np
import sys

from scipy.stats import zscore
from scipy.linalg import orth
from numpy.linalg import pinv

#sys.path.append("..")
from bls.processing.result import result
from bls.processing.sparse_bls import sparse_bls

from sklearn import preprocessing
from bls.processing.mapminmax import mapminmax

from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

"""
    Function that creates the BLS model. It returns the training and test accuracy, training and
    testing time, and testing F-Score.
        bls_train_fscore(train_x, train_y, test_x, test_y, s, C, N1, N2, N3)
        'train_x' and 'test_x' are the entire training data and test data.
        'train_y' and 'test_y' are the entire training labels and test labels.
        's' is the shrinkage parameter for enhancement nodes.
        'C' is the parameter for sparse regularization.
        'N1' is the number of mapped feature nodes.
        'N2' are the groups of mapped features.
        'N3' is the number of enhancement nodes.
    
    Randomoly generated weights for the mapped features and enhancement nodes are
    stored in the
    matrices 'we' and 'wh,' respectively.
"""
def bls_train_fscore(train_x, train_y, test_x, test_y, s, C, N1, N2, N3):

    # Training - begin
    time_start=time.time()
    beta11 = [];

    train_x = zscore(train_x.transpose(), axis = 0, ddof = 1).transpose();
    H1 = np.concatenate((train_x, 0.1 * np.ones((train_x.shape[0], 1))), axis=1);

    y = np.zeros((train_x.shape[0], N2 * N1));

    max_list_set = [];
    min_list_set = [];

    ### Generation of mapped features
    for i in range(0, N2):
        
        #we = 2.0 * np.random.rand(train_x.shape[1] + 1, N1) - 1.0;
        we = 2.0 * np.random.rand(N1, train_x.shape[1] + 1).transpose() - 1.0;
        
        #we = np.loadtxt("we.csv", delimiter = ",");
        #np.savetxt("we.csv", we, delimiter=",");

        A1 = np.dot(H1, we);
        [A1, max_list, min_list] = mapminmax(A1);
        del we;

        beta1 = sparse_bls(A1, H1, 1e-3, 50).transpose();
        beta11.append(beta1);
        T1 = np.dot(H1, beta1);

        print("Feature nodes in window ", i, ": Max Val of Output ", T1.max(), " Min Val ", T1.min());

        [T1, max_list, min_list] = mapminmax(T1.transpose(), 0, 1);
        T1 = T1.transpose();

        max_list_set.append(max_list);
        min_list_set.append(min_list);

        y[:, N1 * i: N1 * (i + 1)] = T1;

    del H1;
    del T1;

    ### Generation of enhancement nodes
    H2 = np.concatenate((y, 0.1 * np.ones((y.shape[0], 1))), axis=1);

    if N1 * N2 >= N3:
        #wh = orth(2 * np.random.rand(N2 * N1 + 1, N3) - 1);
        wh = orth(2 * np.random.rand(N3, N2 * N1 + 1).transpose() - 1);

    else:
        #wh = orth(2 * np.random.rand(N2 * N1 + 1, N3).transpose() - 1).transpose();
        wh = orth(2 * np.random.rand(N3, N2 * N1 + 1) - 1).transpose();

    #wh = np.loadtxt("wh.csv", delimiter = ",");
    #np.savetxt("wh.csv", wh, delimiter=",");

    T2 = np.dot(H2, wh);
    l2 = T2.max();
    l2 = s * 1.0 / l2;

    print("Enhancement nodes: Max Val of Output ", l2, " Min Val ", T2.min());

    T2 = np.tanh(T2 * l2);
    T3 = np.concatenate((y, T2), axis=1);

    del H2;
    del T2;

    # Moore-Penrose pseudoinverse (function pinv)
    beta = np.dot(pinv(np.dot(T3.transpose(), T3) + np.identity(T3.transpose().shape[0]) * C),
        np.dot(T3.transpose(), train_y));
    
    xx = np.dot(T3, beta);

    del T3;

    time_end=time.time()
    Training_time = time_end - time_start
    
    # Training - end

    print("Training has been finished!");
    print("The Total Training Time is : ", Training_time, " seconds");

    ### Training Accuracy
    yy = result(xx);
    train_yy = result(train_y);

    cnt = 0;
    for i in range(0, len(yy)):
        if yy[i] == train_yy[i]:
            cnt = cnt + 1;

    TrainingAccuracy = cnt * 1.0 / train_yy.shape[0];

    print("Training Accuracy is : ", TrainingAccuracy * 100, " %");

    ### Testing Process
    # Testing - begin
    time_start=time.time()
    test_x = zscore( np.float128(test_x).transpose() ,axis = 0, ddof = 1).transpose();
        
    HH1 = np.concatenate((test_x, 0.1 * np.ones((test_x.shape[0], 1))), axis=1);
    yy1 = np.zeros((test_x.shape[0], N2 * N1));

    ### Generation of mapped features
    for i in range(0, N2):

        beta1 = beta11[i];

        TT1 = np.dot( np.float128(HH1), np.float128(beta1)) ;

        max_list = max_list_set[i];
        min_list = min_list_set[i];

        [TT1, max_list, min_list] = mapminmax( TT1.transpose(), 0, 1, max_list, min_list);
        TT1 = TT1.transpose();

        del beta1;
        del max_list;
        del min_list;

        yy1[:, N1 * i: N1 * (i + 1)] = TT1;

    del TT1;
    del HH1;

    ### Generation of enhancement nodes
    HH2 = np.concatenate((yy1, 0.1 * np.ones((yy1.shape[0], 1))), axis=1);
    TT2 = np.tanh(np.dot(HH2, wh) * l2);


    TT3 = np.concatenate((yy1, TT2), axis=1);

    del HH2;
    del wh;
    del TT2;

    x = np.dot(TT3, beta);

    time_end=time.time()
    Testing_time = time_end - time_start

    # Testing - end

    print("Testing has been finished!");
    print("The Total Testing Time is : ", Testing_time, " seconds");

    ### Testing accuracy
    y = result(x);
    test_yy = result(test_y);

    cnt = 0;
    for i in range(0, len(y)):
        if y[i] == test_yy[i]:
            cnt = cnt + 1;

    TestingAccuracy = cnt * 1.0 / test_yy.shape[0];

    label = test_yy;
    predicted = y;

    TestingAccuracy = accuracy_score(label, predicted)
    f_score = f1_score(label, predicted)

    del TT3;

    print("Testing Accuracy is : ", TestingAccuracy * 100, " %");
    print("Testing F-Score is : ", f_score * 100, " %");

    return TrainingAccuracy, TestingAccuracy, Training_time, Testing_time, f_score;
