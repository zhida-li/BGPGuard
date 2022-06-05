"""
    @authors Zhida Li
    @email zhidal@sfu.ca
    @date Oct. 18, 2020
    @version: 1.0.0
    @description:
                GBDT: final testing
    @copyright Copyright (c) Oct. 18, 2020
        All Rights Reserved
    @date edited: June 12, 2021
"""

# print(__doc__)

# ==============================================
# main file: For final testing
# ==============================================
# Last modified: May. 13, 2022


# Import Python libraries
import os
import sys
import time
import warnings

# import pandas as pd
import numpy as np
from scipy.stats import zscore

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

# import lightgbm as lbg
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

# Import customized libraries
# sys.path.append('./')
from journalLib.replaceNan import replaceNan
from journalLib.feature_select_cnl import feature_select_cnl
from journalLib.metrics_cnl import confusion_matrix_cnl

np.seterr(divide='ignore', invalid='ignore')


# warnings.filterwarnings('ignore')


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


#######################################################################
# GBDT parameters: list format. Order: 'all', 16, 8 or 'all', 64, 32
# Parameters from "lightgbm_param_final_slammer.csv"
num_estimators = [300, 100, 300]  # <-- specify no. of estimators for 'all', 16, 8 features
learn_rate = [0.05, 0.1, 0.05]  # <-- specify learning rates for 'all', 16, 8 features

dataset = 'slammer'  # <-- specify datasets
algo_gbm = 'lightgbm'  # xgboost, lightgbm, catboost  # <-- change algorithms

# Combine the parameters
total_exp_features_bgp = ['all', 16, 8]  # <-- 3 cases of the most relevant features
total_exp_features_nslcic = ['all']  # , 64, 32]  # <-- for other data, may ignore

#######################################################################

if dataset == 'slammer' or dataset == 'nimda' or dataset == 'codered1':
    elnList = zip(num_estimators, learn_rate, total_exp_features_bgp)
else:
    elnList = zip(num_estimators, learn_rate, total_exp_features_nslcic)

print('------ Start ------')
result_save = []
head = ['Dataset and number of selected features', 'Accuracy', 'F-Score',
        'Precision', 'Sensitivity', 'TP', 'FN', 'FP', 'TN', 'Training time']
for estNum, lr, n in elnList:
    # Load the datasets
    if dataset == 'slammer':
        train_dataset = np.loadtxt('./datasets/slammer_64_train.csv', delimiter=',')
        test_dataset = np.loadtxt('./datasets/slammer_64_test.csv', delimiter=',')
    else:
        print('Re-enter the dataset')
        exit()

    train_x = train_dataset[:, 0:-1]
    # print(train_x.shape)
    if dataset == 'cicids17' or dataset == 'cicids18' or dataset == 'cicids19':
        pass
    else:
        # train_x = zscore(train_x, axis=0, ddof=1)
        pass
    replaceNan(train_x)
    train_y = train_dataset[:, -1]

    # Change training labels
    inds1 = np.where(train_y == 0)
    train_y[inds1] = 2

    test_x = test_dataset[:, 0:-1]
    if dataset == 'cicids17' or dataset == 'cicids18' or dataset == 'cicids19':
        pass
    else:
        # test_x = zscore(test_x, axis=0, ddof=1)
        pass
    replaceNan(test_x)
    test_y = test_dataset[:, -1]

    # Change test labels
    inds2 = np.where(test_y == 0)
    test_y[inds2] = 2

    # ### feature selection - begin
    if n == 'all':
        pass
    else:
        features = feature_select_cnl(train_x, train_y, n)
        train_x = train_x[:, features]
        test_x = test_x[:, features]
    # ### feature selection - end

    X = train_x
    Y = train_y

    Xx = test_x
    Yy = test_y

    # Training
    time_start = time.time()
    if algo_gbm == 'lightgbm':
        # gbm = LGBMClassifier(n_estimators=estNum, learning_rate=lr)
        # gbm = LGBMClassifier(n_estimators=estNum, learning_rate=lr, max_depth=-1, subsample=1, num_leaves=31,
        #                      boosting_type='gbdt', reg_lambda=0)  #
        gbm = LGBMClassifier(n_estimators=estNum, learning_rate=lr, max_depth=10, subsample=1, num_leaves=20,
                             boosting_type='gbdt', reg_lambda=0)  #
    elif algo_gbm == 'xgboost':
        gbm = XGBClassifier(n_estimators=estNum, learning_rate=lr, max_depth=6, subsample=1,
                            booster='gbtree')  #
    elif algo_gbm == 'catboost':
        gbm = CatBoostClassifier(n_estimators=estNum, learning_rate=lr, max_depth=6, subsample=1, num_leaves=31,
                                 boosting_type='Plain')  # or Ordered, Plain type
    else:
        print('Re-enter the algorithm')
        exit()

    gbm.fit(X, Y.ravel())
    time_end = time.time()
    trainingTime = time_end - time_start

    # Testing
    predicted = gbm.predict(Xx)
    # Test Results
    accuracy = accuracy_score(Yy, predicted)
    fscore = f1_score(Yy, predicted)
    precision = precision_score(Yy, predicted)
    sensitivity = recall_score(Yy, predicted)
    tp, fn, fp, tn = confusion_matrix_cnl(Yy, predicted)

    result_append = ['{}_{}_{}'.format(algo_gbm, dataset, n),
                     '{:.6f}'.format(accuracy * 100), '{:.6f}'.format(fscore * 100),
                     '{:.6f}'.format(precision * 100), '{:.6f}'.format(sensitivity * 100),
                     '{}'.format(tp), '{}'.format(fn), '{}'.format(fp), '{}'.format(tn), '{}'.format(trainingTime)]

    result_save.append(result_append)

result_save = np.asarray(result_save)
head = np.array(head)
head = head.reshape((1, len(head)))
result_save = np.concatenate((head, result_save), axis=0)
# Save final results for each dataset
np.savetxt('%s_results_%s.csv' % (algo_gbm, dataset),
           result_save, fmt='%s',
           delimiter=',')
print('------ Results have been saved to %s_results_%s.csv ------' % (algo_gbm, dataset))

print('------ Completed ------')
