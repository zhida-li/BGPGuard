# -*- coding: utf-8 -*-
"""
@author Zhida Li <zhidal@sfu.ca>
@date Aug. 08, 2019

@copyright Copyright (c) Jan. 12, 2020                    ZHIDA LI
    All Rights Reserved
"""
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from scipy.stats import zscore


def feature_select_cnl(data, label, top_f_features):
    # np.random.seed(1);
    model = ExtraTreesClassifier(n_estimators=100, random_state=1)
    label = np.ravel(label)
    model.fit(data, label)

    importances = model.feature_importances_
    # print(importances)

    f_indices = np.argsort(importances)[::-1]
    # print(f_indices)

    selected_features = f_indices[0:top_f_features]
    # print(selected_features)

    # importances2 = importances[selected_features]
    # print(importances2)

    # output = np.concatenate((selected_features.reshape((-1,1)), importances2.reshape((-1,1))),axis=1)
    # np.savetxt('featureImportance_nslkdd.csv', output, delimiter=',' , fmt='%f')

    return selected_features
