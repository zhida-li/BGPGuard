"""
    @authors Zhida Li
    @email zhidal@sfu.ca
    @date Oct. 17, 2020
    @version: 1.0.0
    @description:
                LightGBM: Best set of the parameters extraction from cross-validation
    @copyright Copyright (c) Oct. 17, 2020
        All Rights Reserved
"""

# print(__doc__)

import numpy as np


# GBDT parameters
# NUM_ESTIMATORS = [10, 20]
# LEARN_RATE = [0.01, 0.05]

# Function -- begin
def best_parameter_extraction(num_estimators, learn_rate, algo_gbm='lightgbm', dataset='slammer', num_features='all'):
    elList = []
    for gg in learn_rate:
        for CC in num_estimators:
            list0 = [CC, gg]
            elList.append(list0)

    index_gbm = 1
    val_acc_mean_gbm = 0
    param_gbm = ''
    result_gbm = []
    for estNum, lr in elList:
        # Load files
        val_acc = np.loadtxt('./tempAcc_%s_%s_%s/train_acc' % (algo_gbm, dataset, num_features)
                             + str(estNum) + str(lr) + '.csv',
                             delimiter=",")
        val_acc_mean = val_acc[-1]

        if index_gbm == 1:
            val_acc_mean_gbm = val_acc_mean
            param_gbm = str(estNum) + '_' + str(lr)
            num_estimators_best, learn_rate_best = estNum, lr
        else:
            if val_acc_mean > val_acc_mean_gbm:
                val_acc_mean_gbm = val_acc_mean
                param_gbm = str(estNum) + '_' + str(lr)
                num_estimators_best, learn_rate_best = estNum, lr
        index_gbm += 1
    # print(val_acc_mean)

    print('%s' % algo_gbm, val_acc_mean_gbm, param_gbm)
    result_gbm = [['%s' % algo_gbm, str(val_acc_mean_gbm), param_gbm]]

    result = np.asarray(result_gbm)
    # print(result)

    # np.savetxt('BestResult_acc_lightgbm_%s_%s.csv' % (dataset, num_features),
    #            result, fmt=['%s', '%s', '%s'],
    #            delimiter=',', )

    results_all = ['BestResult_acc_%s_%s_%s.csv' % (algo_gbm, dataset, num_features),
                   {'num_estimators_best': num_estimators_best, 'learn_rate_best': learn_rate_best}]
    return num_estimators_best, learn_rate_best, val_acc_mean_gbm, results_all  # Output: three parameters, one dict

# Function -- end
