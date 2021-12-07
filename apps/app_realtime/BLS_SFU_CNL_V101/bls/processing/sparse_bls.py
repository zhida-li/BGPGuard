"""
    @authors: Zhida Li, Ana Laura Gonzalez Rios, and Guangyu Xu
    @email: {zhidal, anag, gxa5}@sfu.ca
    @date: Sept. 14, 2019
    @version: 1.0.0
    @description:
                This library contains the functions 'shrinkage' and 'sparse_bls.'
                It returns the weights for getting sparse mapped features.

    @copyright Copyright (c) Sept. 14, 2019
        All Rights Reserved

    This Python code (version 3.6) is a translated from MATLAB code (version R2019b).
    (http://www.broadlearning.ai/).
"""

######################################################
####### Sparse BLS
######################################################

# Import the Python libraries
import numpy as np

from scipy.stats import zscore
from numpy.linalg import solve

"""
    Function that shrinks a value 'x' and returns the shrinked value'z.'
        shrinkage(x,kappa)
        'x' is the value that will be shrinked.
        'kappa' is the shrinkage parameter.
"""


def shrinkage(x, kappa):
    m1 = x - kappa;
    m2 = -1 * x - kappa;

    for i in range(0, len(m1)):
        for j in range(0, len(m1[i, :])):
            if m1[i, j] < 0:
                m1[i, j] = 0.0;

    for i in range(0, len(m2)):
        for j in range(0, len(m2[i, :])):
            if m2[i, j] < 0:
                m2[i, j] = 0.0;

    z = m1 - m2;
    return z;

"""
Function that (write purpose of funciton here). It returns 'wk.'
sparce_bls(A, b, lam, itrs)
'A' is a matrix with the output of the function mapminmax in the generation of mapped
features.
'b' is the original data points of the trainining dataset.
'lam' is 1e-3 (default).
'itrs' is 50  (default).
"""


def sparse_bls(A, b, lam, itrs):
    AA = np.dot(A.transpose(), A);

    m = A.shape[1];
    n = b.shape[1];
    x = np.zeros((m, n));

    wk = x;
    ok = x;
    uk = x;

    L1 = solve((AA + np.identity(m)), np.identity(m));

    L2 = np.dot(np.dot(L1, A.transpose()), b);

    for i in range(0, itrs):
        tempc = ok - uk;
        ck = L2 + np.dot(L1, tempc);
        ok = shrinkage(ck + uk, lam);
        uk = uk + (ck - ok);
        wk = ok;

    return wk;
