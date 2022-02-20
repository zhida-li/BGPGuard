# Use the generated out.txt to get the length of the labels
# May. 04, 2020

import numpy as np


## Input
# output_file_out_txt from feature_extractor_multi() function
# DUMP_YYYYMMDD_out.txt
# output_file_list = ["DUMP_20030123_out.txt","DUMP_20030124_out.txt","DUMP_20030125_out.txt",
# 					"DUMP_20030126_out.txt","DUMP_20030127_out.txt"]
# site = 'RIPE'

# start_date_anomaly = '20030125' 
# end_date_anomaly = '20030125'
# start_time_anomaly = '0531' #869 ones
# end_time_anomaly = '1959'

def label_generator(start_date_anomaly, end_date_anomaly, start_time_anomaly, end_time_anomaly, site, output_file_list):
    # Maybe need a step to verify if end_date_anomaly > end_date_anomaly
    # def label_generator():
    print("--------------------Label Generation-Begin--------------------")
    ## Verify if anomalous start and end dates are in the output_file_list.
    if 'DUMP_%s_out.txt' % start_date_anomaly and 'DUMP_%s_out.txt' % end_date_anomaly in output_file_list:
        start_date_anomaly_list_index = output_file_list.index('DUMP_%s_out.txt' % start_date_anomaly)
        end_date_anomaly_list_index = output_file_list.index('DUMP_%s_out.txt' % end_date_anomaly)
        print("Input date verification: Pass")
        pass
    else:
        print("Please re-enter anomalous start date or end date.")
        exit()

    ## Check the total number of data points
    # Load all txt files
    d = {}  # use dictionary
    for i, DUMPout in enumerate(output_file_list):
        if i == 0:
            d["DUMPout_%d" % i] = np.loadtxt("./data_split/%s" % output_file_list[i])
            matrix = d["DUMPout_%d" % i]
        else:
            d["DUMPout_%d" % i] = np.loadtxt("./data_split/%s" % output_file_list[i])
            matrix1 = d["DUMPout_%d" % i]
            matrix = np.append(matrix, matrix1, axis=0)
    # print('d keys: ', d.keys())  # class: dict_keys

    # Select 37 features / 41 features
    start_featrue = 5 - 1
    matrix = matrix[:, start_featrue:]

    # Check if individual file check needed
    if matrix.shape[0] % 1440 == 0:
        # print("matrix shape:", matrix.shape)
        pass
    else:
        print("Check if individual out.txt file")
        exit()

    ## Initialize labels with zeros
    labels = np.zeros((matrix.shape[0], 1))

    # Create labels for anomaly == ones
    # print(start_date_anomaly_list_index)
    # print(end_date_anomaly_list_index)
    # Check if the anomalous event is in one day or otherwise
    start_point_anomaly = int(start_time_anomaly[0:2]) * 60 + int(start_time_anomaly[2:])
    end_point_anomaly = int(end_time_anomaly[0:2]) * 60 + int(end_time_anomaly[2:])

    labels_anomaly_index_start = start_date_anomaly_list_index * 1440 + start_point_anomaly
    labels_anomaly_index_end = end_date_anomaly_list_index * 1440 + end_point_anomaly  # This index should be included for anomaly

    labels[labels_anomaly_index_start:(labels_anomaly_index_end + 1),
    0] = 1  # +1 because labels_anomaly_index_end should be included

    # print(labels_anomaly_index_start)
    # print(labels_anomaly_index_end)

    # Get the number of anomaly
    # num_anomaly = len(np.where(labels==1)[0])  # May be returned
    # print("Number of anomaly:", num_anomaly)
    np.savetxt('./STAT/labels_%s.csv' % site, labels, delimiter=',', fmt='%d')

    print("--------------------Label Generation-end----------------------\n")

    return labels
