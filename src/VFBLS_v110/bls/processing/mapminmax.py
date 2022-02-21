"""
    @authors: Zhida Li, Ana Laura Gonzalez Rios, and Guangyu Xu
    @email: {zhidal, anag, gxa5}@sfu.ca
    @date: Sept. 14, 2019
    @version: 1.0.0
    @version: 1.0.0
    @description:
        This library contains the class My_MinMaxScaller(MinMaxScaler). The class is
        conformed by the functions '__init__,' 'my_fit,' and 'mapminmax.'
        It maps the row minimum and maximum values to [min_val max_val] using the input matrix.
        The input matrix has only finite real values.
        The Mapminmax function also returns the minimum and maximum values of the input matrix.

    @copyright Copyright (c) Sept. 14, 2019
        All Rights Reserved

    This Python code (version 3.6) is implemented based on MATLAB function mapminmax
    (https://www.mathworks.com/help/deeplearning/ref/mapminmax.html).

"""

######################################################
####### Mapminmax
######################################################

# Import the Python libraries
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
import numpy as np


class My_MinMaxScaler(MinMaxScaler):

    def __init__(self, feature_range=(0, 1), copy=True):
        MinMaxScaler.__init__(self, feature_range);

    """
    Function that scales an input matrix.
        my_fit(self, X, y=None, my_data_min=None, my_data_max=None, min_val=-1, max_val=1)
        'X' is the input data matrix.
        'y' is the output matrix. It is initialized with the value "None."
        'my_data_min' is the initial minimum value. It is initialized with the value "None."
        'my_data_max' is the initial minimum value. It is initialized with the value "None."
        'min_val' is the minimum value of each row in 'X'. It is initialized with the value "-1."
        'max_val' is the maximum value of each row 'X'. It is initialized with the value "1."
    """

    def my_fit(self, X, y=None, my_data_min=None, my_data_max=None, min_val=-1, max_val=1):

        data_min = np.array(my_data_min);
        my_data_max = np.array(my_data_max);
        data_range = my_data_max - data_min;

        # Do not scale constant features
        if isinstance(data_range, np.ndarray):
            data_range[data_range == 0.0] = 1.0
        elif data_range == 0.:
            data_range = 1
        self.scale_ = (max_val - min_val) / data_range
        self.min_ = min_val - data_min * self.scale_
        self.data_range = data_range
        self.data_min = data_min
        return self

    """
    Function that maps the row minimum and maximum values to [-v_min v_max]. It returns
    'matrix,' 'max_list,' and 'min_list' (explain matrix, max_list, and min_list)
        mapminmax(matrix, v_min = -1, v_max = 1, l_max = None, l_min = None)
        'matrix' is the input matrix.
        'v_min' is the row minimum value. It is initialized with the value "-1."
        'v_max' is the row maximum value. It is initialized with the value "1."
        'l_max' is used in the initalize max_list. It is initialized with the value "None."
        'l_min' is used to initialize min_list. It is initialized with the value "None."
    """


def mapminmax(matrix, v_min=-1, v_max=1, l_max=None, l_min=None):
    max_list = [];
    min_list = [];

    if l_max is None and l_min is None:
        max_list = np.max(matrix, axis=1);
        min_list = np.min(matrix, axis=1);
        matrix = matrix.astype(float);
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(v_min, v_max));
        matrix = min_max_scaler.fit_transform(matrix.transpose()).transpose();
    else:
        matrix = matrix.astype(float);
        min_max_scaler = My_MinMaxScaler(feature_range=(v_min, v_max));
        min_max_scaler.my_fit(X=matrix, my_data_min=l_min, my_data_max=l_max, min_val=v_min, max_val=v_max);
        matrix = min_max_scaler.transform(matrix.transpose()).transpose();

    return matrix, max_list, min_list;
