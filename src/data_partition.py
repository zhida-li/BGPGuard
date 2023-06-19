# Data partition for DUMP_out.txt 
# csv files will be generated and saved to data_split folder.
# May. 06, 2020

import numpy as np
from label_generation import label_generator


# output_file_out_txt from feature_extractor_multi() function
# DUMP_YYYYMMDD_out.txt

# output_file_list = ["DUMP_20030123_out.txt","DUMP_20030124_out.txt","DUMP_20030125_out.txt",
# 					"DUMP_20030126_out.txt","DUMP_20030127_out.txt"]

# # Partition percentage
# cut_pct = '64'
# site = 'RIPE'
# rnn_seq = 20

def data_partition(cut_pct, site, output_file_list, labels, rnn_seq=1):
    print("--------------------Data Partition-Begin----------------------")
    # Load txt files for each day
    d = {}  # use dictionary

    # matrix = np.array([])
    for i, DUMPout in enumerate(output_file_list):
        if i == 0:
            d["DUMPout_%d" % i] = np.loadtxt("./src/data_split/%s" % output_file_list[i])
            matrix = d["DUMPout_%d" % i]
        else:
            d["DUMPout_%d" % i] = np.loadtxt("./src/data_split/%s" % output_file_list[i])
            matrix1 = d["DUMPout_%d" % i]
            matrix = np.append(matrix, matrix1, axis=0)
    # print('d keys: ', d.keys())  # class: dict_keys

    # Select 37 features / 41 features
    start_featrue = 5 - 1
    matrix = matrix[:, start_featrue:]
    print('matrix shape:', matrix.shape)  # if shape, type = <class 'tuple'>, if shape[1], type = <class 'int'>

    # Statistics of the dataset
    inds1 = np.where(labels == 1);  # index of anomalies
    dataset_Stat = [matrix.shape[0], len(inds1[0]), 0, 0, 0];
    print("The processing dataset has %d data points, with %d anomaly inside." % (dataset_Stat[0], dataset_Stat[1]))

    # print("---------------------------------------------------------")
    # Find the cutting point

    dataset_Stat[2] = round(dataset_Stat[1] * float(int(cut_pct[0]) / 10));  # np.round return float...percentage
    # print("Dataset %s/%s cut at index %d of the anomaly set."% (cut_pct[0], cut_pct[1], dataset_Stat[2]-1))  # dataset_Stat[2] cut point in anomaly

    # print("---------------------------------------------------------")

    # Merge matrix and labels
    dataset = np.concatenate((matrix, labels), axis=1)

    # Cut
    anomaly_index = inds1[0]
    # print(anomaly_index)
    cut_index = anomaly_index[dataset_Stat[2] - 1]  # cut after cut_index, start from index 0, thats why -1
    # print("Cutting index will be included: ",cut_index)

    if (cut_index + 1) % rnn_seq == 0:
        cut_index_fix = cut_index + 1
    else:
        cut_index_fix = (rnn_seq - (cut_index + 1) % rnn_seq) + cut_index + 1;
    print('Cutting data point:', cut_index_fix)

    # train test
    # train = dataset[0:(cut_index+1), :]  # +1 because the point cut_index should be counted
    # test = dataset[(cut_index+1):, :]
    train = dataset[0:cut_index_fix, :]  # +1 because the point cut_index should be counted
    test = dataset[cut_index_fix:, :]

    np.savetxt('./src/data_split/train_%s_%s.csv' % (cut_pct, site), train, delimiter=',')  # ,fmt='%.4f')
    np.savetxt('./src/data_split/test_%s_%s.csv' % (cut_pct, site), test, delimiter=',')  # ,fmt='%.4f')

    # Calculate number of regular and anomalous data points for train and test
    num_regular_train = len(np.where(train[:, -1] == 0)[0])
    num_regular_test = len(np.where(test[:, -1] == 0)[0])

    num_anomaly_train = len(np.where(train[:, -1] == 1)[0])
    num_anomaly_test = len(np.where(test[:, -1] == 1)[0])

    toal_number_train = num_anomaly_train + num_regular_train
    toal_number_test = num_anomaly_test + num_regular_test

    train_test_stat = ["No. of data points in train:", toal_number_train, '\n',
                       "No. of data points in test:", toal_number_test, '\n',
                       "No. of regular data points in train:", num_regular_train, '\n',
                       "No. of regular data points in test:", num_regular_test, '\n',
                       "No. of anomaly data points in train:", num_anomaly_train, '\n',
                       "No. of anomaly data points in test:", num_anomaly_test, '\n']

    train_test_stat = np.array(train_test_stat)
    np.savetxt('./src/STAT/train_test_stat.txt', train_test_stat, delimiter=',', fmt='%s')

    print("--------------------Data Partition-End-------Files saved------\n")

    '''
    Has problem for dimension match:
    result_array = np.array([])
    for line in data_array:
    	result = do_stuff(line)
    	result_array = np.append(result_array, result)
    '''
