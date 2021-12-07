"""
    @authors Zhida Li, Ana Laura Gonzalez Rios, and Guangyu Xu
    @email {zhidal, anag, gxa5}@sfu.ca
    @date Sept. 14, 2019
    @version: 1.0.0
    @description:
                This library contains the function 'result.'
                It returns a column vector (labels) with the values 1, 2, or/and 3 ... n. 

    @copyright Copyright (c) Sept. 14, 2019
        All Rights Reserved

    This Python code (version 3.6) is translated from MATLAB code (version R2019b).
    (http://www.broadlearning.ai/).
"""

######################################################
####### Result
######################################################

# Import the Python library
import numpy as np

"""
    Function that decodes the lables predicted using BLS algorithms. It returns 'ret' (a column
    vector for labels).
        result(x)
        'x' are the labels with 'n' columns, where 'n' is the number of the classes
"""
def result(x):
	ret = np.zeros( (1, x.shape[0]) );

	for i in range(0, x.shape[0]):

		v_max = float("-inf");
		v_ind = 0;
		
		for j in range(0, x.shape[1]):
			if v_max < x[i, j]:
				v_max = x[i, j];
				v_ind = j;

		ret[0, i] = v_ind + 1;

	ret = ret.transpose();

	return ret;

