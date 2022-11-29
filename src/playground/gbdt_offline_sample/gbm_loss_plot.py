"""
    @authors Zhida Li
    @email zhidal@sfu.ca
    @date Nov. 16, 2022
    @version: 1.0.1
    @description:
                GBDT: loss plotting
    @copyright Copyright (c) Nov. 16, 2022
        All Rights Reserved
    @date edited: Nov. 16, 2022
"""

# print(__doc__)

# ==============================================
# File: For plotting GBDT loss
# ==============================================
# Last modified: Nov. 28, 2022

# Import Python libraries
import sys
import math
import warnings
import time
import random

import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.metrics import f1_score

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
# from sklearn.ensemble import GradientBoostingClassifier

# Import customized libraries
from journalLib.replaceNan import replaceNan

# Loading datasets
train_dataset = np.loadtxt('./datasets/slammer_64_train.csv', delimiter=',')
test_dataset = np.loadtxt('./datasets/slammer_64_test.csv', delimiter=',')

train_x = train_dataset[:, 0:-1]
replaceNan(train_x)
train_y = train_dataset[:, -1]

test_x = test_dataset[:, 0:-1]
replaceNan(test_x)
test_y = test_dataset[:, -1]

X = train_x
Y = train_y

Xx = test_x
Yy = test_y

#######################################################################
# GBDT parameters
NUM_ESTIMATORS = 300
LEARN_RATE = 0.01

# GBM algorithm
# algo_gbm = 'lightgbm'  # xgboost, lightgbm, catboost
print('Choose a GBM: xgboost, lightgbm, catboost')
algo_gbm =  input('GBM: ')

algo_list = ['xgboost', 'lightgbm', 'catboost']
if algo_gbm not in algo_list:
    print("Please re-enter the GBM.")
    exit()

# Training
time_start = time.time()

if algo_gbm == 'xgboost':
    gbm = XGBClassifier(learning_rate=LEARN_RATE, n_estimators=NUM_ESTIMATORS, max_depth=6, subsample=1,
                        booster='gbtree')  #
elif algo_gbm == 'lightgbm':
    gbm = LGBMClassifier(learning_rate=LEARN_RATE, n_estimators=NUM_ESTIMATORS)
    # gbm.fit(X, Y.ravel(), eval_set=eval_set_train_valid, eval_metric='logloss')

elif algo_gbm == 'catboost':
    gbm = CatBoostClassifier(learning_rate=LEARN_RATE, n_estimators=NUM_ESTIMATORS, max_depth=6, subsample=1, num_leaves=31,
                             boosting_type='Plain')  # or Ordered, Plain type

eval_set_train_valid = [(X, Y.ravel()), (Xx, Yy.ravel())]
gbm.fit(X, Y.ravel(), eval_set=eval_set_train_valid)
# gbm.fit(X, Y.ravel())
time_end = time.time()

# Testing
predicted_gbm = gbm.predict(Xx)

# Results
accuracy_gbm = metrics.accuracy_score(Yy, predicted_gbm)
fscore_gbm = f1_score(Yy, predicted_gbm)
trainingTime_gbm = time_end - time_start
trainingTime = trainingTime_gbm
print('Accuracy:', accuracy_gbm, '\n',
      'F-Score:', fscore_gbm, '\n',
      'Training time:', trainingTime_gbm)

# Plotting logloss: -log P(yt|yp) = -(yt log(yp) + (1 - yt) log(1 - yp))
results = gbm.evals_result_  # dict
if algo_gbm == 'xgboost':
    epochs = len(results['validation_0']['logloss'])
elif algo_gbm == 'lightgbm':
    epochs = len(results['valid_0']['binary_logloss'])
elif algo_gbm == 'catboost':
    epochs = len(results['validation_0']['Logloss'])

x_axis = range(0, epochs)
# plot log loss
if algo_gbm == 'xgboost':
    plt.plot(x_axis, results['validation_0']['logloss'], label='Train')
    plt.plot(x_axis, results['validation_1']['logloss'], label='Valid')
elif algo_gbm == 'lightgbm':
    plt.plot(x_axis, results['valid_0']['binary_logloss'], label='Train')
    plt.plot(x_axis, results['valid_1']['binary_logloss'], label='Valid')
elif algo_gbm == 'catboost':
    plt.plot(x_axis, results['validation_0']['Logloss'], label='Train')
    plt.plot(x_axis, results['validation_1']['Logloss'], label='Valid')

plt.legend()
plt.xlabel('Number of estimators')
plt.ylabel('Log Loss')
plt.title('%s Log Loss' % algo_gbm)
plt.show()

