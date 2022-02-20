"""
    @authors Zhida Li, Ana Laura Gonzalez Rios, and Guangyu Xu
    @email {zhidal, anag, gxa5}@sfu.ca
    @date Sept. 14, 2019
    @version: 1.0.0
    @description:
                This library contains the function 'one_hot_m.'
                It converts the labels with a column vector to a label matrix.
                The values are 1, 2, or/and 3 ... n from the input column vector. 
                This one_hot_m returns label matrix only with 0 and 1.

    @copyright Copyright (c) Sept. 14, 2019
        All Rights Reserved

    This Python code (version 3.6) is implemented for processing one hot encoding.
"""

######################################################
####### One hot encoding
######################################################

# Import the Python library
import numpy as np

"""
    Function that encodes lables based on the number of classes. It assumes that class labels start
    from zero and returns 'ret' (label matrix).
        one_hot_m( y, n_classes)
        'y' is a column matrix that contains the labels of the input data points
        'n_classes' is the number of classes.
"""


def one_hot_m(y, n_classes):
    ret = np.zeros((y.shape[0], n_classes));

    for i in range(0, n_classes):
        for j in range(0, len(y)):
            if y[j] == (i + 1):
                ret[j, i] = 1;

    return ret;
