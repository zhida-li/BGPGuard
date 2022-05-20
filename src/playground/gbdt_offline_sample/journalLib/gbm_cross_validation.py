"""
    @authors Zhida Li
    @email zhidal@sfu.ca
    @date Oct. 17, 2020
    @version: 1.0.0
    @description:
                Cross-validation for IEEE Communications Magazine
    @copyright Copyright (c) Oct. 17, 2020
        All Rights Reserved
    @date edited: June 12, 2021
"""

# print(__doc__)

import os
import sys
import math
import time
import random
import warnings

# import pandas as pd
import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt

# from sklearn import svm
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

# import lightgbm as lbg
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

# sys.path.append('./')
from journalLib.replaceNan import replaceNan
from journalLib.feature_select_cnl import feature_select_cnl
from journalLib.metrics_cnl import confusion_matrix_cnl

# warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings('ignore')


# may Use fscore
# Function -- begin
def gbm_cross_validation(num_estimators, learn_rate, algo_gbm='lightgbm', data_kfold=10,
                         dataset='slammer', num_features='all'):
    # Disable
    def blockPrint():
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def enablePrint():
        sys.stdout = sys.__stdout__

    blockPrint()

    if os.path.exists('tempAcc_%s_%s_%s' % (algo_gbm, dataset, num_features)):
        pass
    else:
        os.mkdir('tempAcc_%s_%s_%s' % (algo_gbm, dataset, num_features))

    # Load train dataset
    if dataset == 'slammer':
        train_dataset0 = np.loadtxt('./datasets/slammer_64_train.csv', delimiter=',')
    else:
        print('Re-enter the dataset')
        exit()

    # NUM_FEATURES = 'all'  # 'all', 16, 8
    # data_kfold = 10
    dataSplit = TimeSeriesSplit(n_splits=data_kfold)  # k-fold cross validation

    # GBDT parameters
    # NUM_ESTIMATORS = [10, 20]
    # LEARN_RATE = [0.01, 0.05]

    elList = []
    for gg in learn_rate:
        for CC in num_estimators:
            list0 = [CC, gg]
            elList.append(list0)
    # number of files will be generated
    num_gen_files = [['Num files will be generated', str(len(elList))]]
    num_gen_files = np.asarray(num_gen_files)
    np.savetxt('./tempAcc_%s_%s_%s/totalNumFiles_%s.csv' % (algo_gbm, dataset, num_features, len(elList)),
               num_gen_files, delimiter=',', fmt=['%s', '%s'])

    index_gbm = 1
    for estNum, lr in elList:
        index = 1
        acc_val_all = np.array([])
        acc_val_all_00 = np.array([])
        acc_val_all_save = np.array([])
        # Extract train and validate data below
        for train_index, val_index in dataSplit.split(train_dataset0):
            print('--------------------------------------------Validation: %d' % index)
            train = train_dataset0[train_index, :]
            validate = train_dataset0[val_index, :]
            train_dataset = train
            test_dataset = validate

            train_x = train_dataset[:, 0:-1]
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
            # Change validation labels
            inds2 = np.where(test_y == 0)
            test_y[inds2] = 2

            # feature selection - begin
            if num_features == 'all':
                pass
            else:
                features = feature_select_cnl(train_x, train_y, num_features)
                train_x = train_x[:, features]
                test_x = test_x[:, features]
            # feature selection - end

            X = train_x
            Y = train_y

            Xx = test_x
            Yy = test_y

            # Training
            time_start = time.time()
            if algo_gbm == 'lightgbm':
                # gbm = LGBMClassifier(n_estimators=estNum, learning_rate=lr)
                gbm = LGBMClassifier(n_estimators=estNum, learning_rate=lr, max_depth=-1, subsample=1, num_leaves=31,
                                     boosting_type='gbdt')  #
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
            # Validation
            predicted = gbm.predict(Xx)
            # Validation Results
            accuracy = accuracy_score(Yy, predicted)
            fscore = f1_score(Yy, predicted)
            fscore = np.float64(fscore)
            # precision = precision_score(Yy, predicted)
            # sensitivity = recall_score(Yy, predicted)
            # tp, fn, fp, tn = confusion_matrix_cnl(Yy, predicted)
            trainingTime = time_end - time_start

            # results = ['LightGBM', '{:.6f}'.format(accuracy * 100), '{:.6f}'.format(fscore * 100),
            #            '{:.6f}'.format(precision * 100), '{:.6f}'.format(sensitivity * 100),
            #            'tp, fn, fp, tn = {}, {}, {}, {}'.format(tp, fn, fp, tn)]
            # print(results)

            acc_val_all_0 = accuracy
            if index == 1:
                acc_val_all = acc_val_all_0.reshape(-1, 1)
            else:
                acc_val_all_00 = acc_val_all_0.reshape(-1, 1)
                acc_val_all = np.append(acc_val_all, acc_val_all_00, axis=1)

            index += 1

        acc_val_all_mean = np.mean(acc_val_all, axis=1)
        acc_val_all_save = np.append(acc_val_all, acc_val_all_mean.reshape(-1, 1), axis=1)

        np.savetxt('./tempAcc_%s_%s_%s/train_acc' % (algo_gbm, dataset, num_features) + str(estNum) + str(lr) + '.csv',
                   acc_val_all_save, delimiter=',', fmt='%.4f')

        index_gbm += 1
    return None  # Output: fsocre may also be used, change line 193 with "fscore"
# Function -- end
