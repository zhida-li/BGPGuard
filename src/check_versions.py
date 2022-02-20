# Checkthe versions of libraries

# Python version
import sys

print('Python: %s' % (sys.version))
# scipy
import scipy

print('scipy: {}'.format(scipy.__version__))
# numpy
import numpy

print('numpy: {}'.format(numpy.__version__))
# matplotlib
import matplotlib

print('matplotlib: {}'.format(matplotlib.__version__))
# scikit-learn
import sklearn

print('sklearn: {}'.format(sklearn.__version__))
import torch

print('PyTorch: {}'.format(torch.__version__))

'''
Python:s 3.6.9 (default, Apr 18 2020, 01:56:04) 
[GCC 8.4.0]
scipy: 1.4.1
numpy: 1.18.4
matplotlib: 3.1.1
sklearn: 0.20.3
PyTorch: 1.1.0
'''
