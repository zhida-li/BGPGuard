# -*- coding: utf-8 -*-
"""
@author Zhida Li <zhidal@sfu.ca>
@date Nov. 28, 2018

@copyright Copyright (c) Nov. 28, 2018                    ZHIDA LI
    All Rights Reserved

"""
######################################################
##### GRU2 (2 hidden layers) using BGP datasets #####
######################################################
# Import the Python libraries
import time

import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import torch.utils.data as Data
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from scipy.stats import zscore

import csv
import os
import sys

sys.path.append('../VFBLS_v110')
from VFBLS_v110.bls.processing.replaceNan import replaceNan

import warnings
warnings.filterwarnings("ignore")

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
# Restore
def enablePrint():
    sys.stdout = sys.__stdout__



def gru2_demo(batch_size=5, RnnTest_path='./data_test', Mdl_path='./RNNMdls'): 
	# Set the seed for generating random numbers on all GPUs.
	torch.manual_seed(1) 
	torch.cuda.manual_seed_all(1)


	### Hyper parameters ####
	parent_dirname = os.path.basename(os.path.dirname(os.path.realpath(__file__)));
	num_feature = 37    # number of the features for input matrix

	#batch_size = 5
	sequence_length = batch_size     # length of the input time sequence
	input_size = num_feature
	input_lstm = num_feature

	hidden_size = 32  # hidden size for fc4
	num_layers = 1    # number of layers for LSTM algorithm
	num_classes = 2   # number of the class


	### Load the datasets, x: data, y: label ####
	# testDataset = np.loadtxt('../data_test/DUMP_out.txt')
	testDataset = np.loadtxt("%s/DUMP_out.txt"%RnnTest_path)
	# testDataset = np.loadtxt("%s/slammer_64_test_ripe.csv"%RnnTest_path, delimiter=",");
	#testDataset = np.loadtxt("slammer_64_test_ripe.csv", delimiter=",");


	# test_data_x = testDataset[:, 4: ];
	test_data_x = testDataset[:, 0:num_feature]
	# Normalize test data

	test_data_x = zscore(test_data_x, axis = 0, ddof = 1);  # For each feature, mean = 0 and std = 1 
	replaceNan(test_data_x);                                # Replace "nan" with 0

	test_label_y = np.zeros((test_data_x.shape[0],1))

	test_len = test_label_y.size;


	# Convert numpy to torch tensor
	test_data_x, test_label_y = torch.from_numpy(test_data_x), torch.from_numpy(test_label_y)

	# Tensor
	# floatTensor for training data, and longTensor for the label
	    # FloatTensor = 32-bit floating
	test_data = test_data_x.type(torch.FloatTensor) 
	test_label = test_label_y.type(torch.LongTensor)





	# Data Loader (Input Pipeline)
	# torch_dataset_train = Data.TensorDataset(data_tensor=train_data,
	#                                         target_tensor=train_label)

	# torch_dataset_test = Data.TensorDataset(data_tensor=test_data,
	#                                         target_tensor=test_label)

	torch_dataset_test = Data.TensorDataset(test_data,test_label)



	#print torch_dataset_train,torch_dataset_test

	test_loader = Data.DataLoader(dataset=torch_dataset_test,
	                              batch_size=batch_size,
	                              shuffle=False)


	#### Build the deep learning models with 2 hidden layers (one layer: GRU, one layer: fc4) ###

	class RNN(nn.Module):
	    def __init__(self):
	        super(RNN, self).__init__()
	        self.hidden_size = hidden_size
	        self.num_layers = num_layers

	        # Define the GRU module
	        self.gru = nn.GRU(input_lstm, hidden_size, num_layers, batch_first=False, dropout=0.4)

	        # Define ReLU layer
	        self.relu = nn.ReLU()

	        # Define the Dropout layer with 0.5 dropout rate
	        self.keke_drop = nn.Dropout(p=0.5)

	        # Define a fully-connected layer fc4 with 32 inputs and 2 outputs
	        self.fc4 = nn.Linear(hidden_size, num_classes)

	    def forward(self, x):
	        # Set initial states: h_0 (num_layers * num_directions, batch, hidden_size)
	        # x=input (seq_len, batch, input_size)
	        
	        if torch.cuda.is_available():
	            h0 = Variable(torch.zeros(self.num_layers, x.size(1), self.hidden_size).cuda())
	        else:
	            h0 = Variable(torch.zeros(self.num_layers, x.size(1), self.hidden_size).cpu())

	        x, _ = self.gru(x, h0)  # GRU network

	        x = self.relu(x)         # ReLU()

	        x = self.fc4(x)          # fully-connected layer
	        return x



	rnn = RNN()
	rnn.train()

	if torch.cuda.is_available():
	    rnn.cuda()
	else:
	    rnn.cpu()


	model_pkl = 'rnn-gru2-%d' % batch_size
	#torch.save(rnn.state_dict(), '%s.pkl'%model_pkl)

	rnn.load_state_dict(torch.load('%s/%s.pkl'%(Mdl_path, model_pkl)))

	start = time.clock()

	### Test the model using evaluation mode ###

	rnn.eval()          # evaluation mode for testing
	yo = []
	for test,l in test_loader:
	    if torch.cuda.is_available():
	        p = Variable(test.view(sequence_length, -1, input_lstm)).cuda()
	    else:
	        p = Variable(test.view(sequence_length, -1, input_lstm))

	        
	    outputs2 = rnn(p)
	    outputs2 = outputs2.view(-1, 2)
	    outputs2 = F.softmax(outputs2)     # softmax function
	    # print 'output2 size:', outputs2.size()

	    _, predicted = torch.max(outputs2.data, 1)
	    if torch.cuda.is_available():
	        predicted = predicted.cpu()
	    predicted_np = predicted.numpy()
	    yo.append(predicted_np)                # predicted labels, yo shape is (1, 72, 100, 1)

	yo = np.array([yo]).reshape(test_len, -1)  
	enablePrint()

	#np.savetxt('./yo.csv', yo, delimiter=',',fmt='%.4f')

	test_hour, test_min = testDataset[:, 1], testDataset[:, 2]
	for label, hour, minute in zip(predicted, test_hour,test_min):
		hour, minute = int(hour), int(minute)
		hour = str(hour)
		if len(hour) == 2:
			pass
		else: 
			hour = '0'+hour
		minute = str(minute)
		if len(minute) == 2:
			pass
		else: 
			minute = '0'+minute
		if label == 1:
			print("\n Test time (hour:minute) %s : %s => An anomaly is detected!" % (hour, minute))
		else:
			print("\n Test time (hour:minute) %s : %s => Normal traffic" % (hour, minute))
	end = time.clock()



