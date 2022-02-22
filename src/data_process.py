# Normalize data and feature selection
# May 06, 2020
import sys
import numpy as np
from scipy.stats import zscore
from sklearn.ensemble import ExtraTreesClassifier

sys.path.append('../VFBLS_v110')
from VFBLS_v110.bls.processing.replaceNan import replaceNan


# cut_pct = '64'
# site = 'RIPE'

# Normalization
def normTrainTest(cut_pct, site):
    train = np.loadtxt('./data_split/train_%s_%s.csv' % (cut_pct, site), delimiter=',')
    test = np.loadtxt('./data_split/test_%s_%s.csv' % (cut_pct, site), delimiter=',')

    train_x = train[:, 0:-1]
    train_x = zscore(train_x, axis=0, ddof=1);  # For each feature, mean = 0 and std = 1
    replaceNan(train_x);
    test_x = test[:, 0:-1]
    test_x = zscore(test_x, axis=0, ddof=1);  # For each feature, mean = 0 and std = 1
    replaceNan(test_x);

    # train_y = train[:,train.shape[1]  - 1 : train.shape[1]];
    # test_y = test[:,test.shape[1]  - 1 : test.shape[1]];
    train_y = train[:, -1]
    test_y = test[:, -1]
    train_y, test_y = train_y.reshape(-1, 1), test_y.reshape(-1, 1)

    # Merge matrix and labels for train and test
    train_n = np.concatenate((train_x, train_y), axis=1)
    test_n = np.concatenate((test_x, test_y), axis=1)

    np.savetxt('./data_split/train_%s_%s_n.csv' % (cut_pct, site), train_n, delimiter=',')  # ,fmt='%.4f')
    np.savetxt('./data_split/test_%s_%s_n.csv' % (cut_pct, site), test_n, delimiter=',')  # ,fmt='%.4f')


# Feature selections:
def featSel(featALGO, data, label, topFeatures=10):
    np.random.seed(1);
    model = ExtraTreesClassifier(n_estimators=100, random_state=1)
    label = np.ravel(label)
    model.fit(data, label)

    importances = model.feature_importances_

    f_indices = np.argsort(importances)[::-1]
    # print(f_indices)

    selected_features = f_indices[0:topFeatures]
    # print(selected_features)
    return selected_features
