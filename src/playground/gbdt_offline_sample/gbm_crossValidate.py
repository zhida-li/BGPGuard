"""
    @authors Zhida Li
    @email zhidal@sfu.ca
    @date Oct. 17, 2020
    @version: 1.0.0
    @description:
                LightGBM: main function for experiment (cross-validation)
    @copyright Copyright (c) Oct. 19, 2020
        All Rights Reserved
    @date edited: June 12, 2021
"""

# print(__doc__)

# ==============================================
# main file: For cross-validation
# ==============================================
# Last modified: May. 13, 2022

# Import Python libraries
import os
import sys

import numpy as np
# Import customized pkg
from journalLib.gbm_cross_validation import gbm_cross_validation
from journalLib.best_parameter_extraction import best_parameter_extraction


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


#######################################################################
# GBDT parameters: list format
# specify the parameters for cross-validation
num_estimators = [10, 50, 100, 200, 300]  # <-- specify no. of estimators
learn_rate = [0.01, 0.05, 0.1]  # <-- specify learning rates

dataset_exp = ['slammer']  # <-- specify datasets, may add more to the list

total_exp_features_bgp = ['all', 16, 8]  # <-- 3 cases of the most relevant features

algo_gbm = 'lightgbm'  # xgboost, lightgbm, catboost  # <-- change algorithms
#######################################################################


if __name__ == '__main__':

    # powerOutage_pk_ripe
    print('------ %s %s experiment start ------' % (algo_gbm, dataset_exp[0]))
    result_save = []
    blockPrint()
    for n in total_exp_features_bgp:
        # Cross-validation use acc
        gbm_cross_validation(num_estimators, learn_rate, algo_gbm=algo_gbm,
                             dataset=dataset_exp[0], num_features=n)
        # Best set of parameters extraction from cross-validation
        num_estimators_best, learn_rate_best, val_acc_mean_gbm, results_all \
            = best_parameter_extraction(num_estimators, learn_rate, algo_gbm=algo_gbm,
                                        dataset=dataset_exp[0],
                                        num_features=n)
        # Save the best set of parameters to the file
        result_append = ['%s_%s_%s' % (algo_gbm, dataset_exp[0], n),
                         str(val_acc_mean_gbm), str(num_estimators_best), str(learn_rate_best)]
        result_save.append(result_append)

    enablePrint()
    result_save = np.asarray(result_save)
    # Save best sets of parameters for feature selections
    np.savetxt('%s_param_final_%s.csv' % (algo_gbm, dataset_exp[0]),
               result_save, fmt='%s',
               delimiter=',')

    print('------ %s %s experiment completed ------ \n' % (algo_gbm, dataset_exp[0]))
