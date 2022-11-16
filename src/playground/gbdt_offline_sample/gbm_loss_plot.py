"""
    @authors Zhida Li
    @email zhidal@sfu.ca
    @date Nov. 16, 2022
    @version: 1.0.0
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
# Last modified: Nov. 16, 2022

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
# import lightgbm as lbg
from lightgbm import LGBMClassifier
from sklearn.ensemble import GradientBoostingClassifier

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

eval_set_train_valid = [(X, Y.ravel()), (Xx, Yy.ravel())]
# Training
time_start = time.time()
gbm = LGBMClassifier(learning_rate=LEARN_RATE, n_estimators=NUM_ESTIMATORS)
gbm.fit(X, Y.ravel(), eval_set=eval_set_train_valid, eval_metric='logloss')
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
results = gbm.evals_result_  # dict for the 'valid_0', 'binary_logloss'
epochs = len(results['valid_0']['binary_logloss'])
x_axis = range(0, epochs)
# plot log loss
plt.plot(x_axis, results['valid_0']['binary_logloss'], label='Train')
plt.plot(x_axis, results['valid_1']['binary_logloss'], label='Valid')
plt.legend()
plt.xlabel('Number of estimators')
plt.ylabel('Log Loss')
plt.title('LightGBM Log Loss')
plt.show()
