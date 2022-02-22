"""
    @authors Zhida Li, Ana Laura Gonzalez Rios, and Guangyu Xu
    @email {zhidal, anag, gxa5}@sfu.ca
    @date Nov. 4, 2019
    @version: 1.0.1
    @description:
                This library contains the function 'one_hot_m.'
                It converts the labels with a column vector to a label matrix.
                The values are 1, 2, or/and 3 ... n from the input column vector. 
                This one_hot_m returns label matrix only with 0 and 1.

    @copyright Copyright (c) Nov. 4, 2019
        All Rights Reserved

    This Python code (version 3.6) is implemented for processing one hot encoding.
"""

######################################################
####### Replace Nan with 0
######################################################
import math
import numpy as np


def replaceNan(matrix):
    for row in range(0, matrix.shape[0]):
        for col in range(0, matrix.shape[1]):

            if math.isnan(matrix[row, col]):
                matrix[row, col] = np.longdouble('0')

    return None

