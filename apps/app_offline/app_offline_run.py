# Run: python3 main.py
# May. 07, 2020
import time
from dataDownload import data_downloader_single
from dataDownload import updateMessageName
from featureExtraction import feature_extractor_single
from time_locator import time_locator_single
from subprocess_cmd import subprocess_cmd

# from RNNMdls.lstm_2layer_load import lstm2_load
# from RNNMdls.lstm_3layer_load import lstm3_load
# from RNNMdls.lstm_4layer_load import lstm4_load
# from RNNMdls.gru_2layer_load import gru2_load
# from RNNMdls.gru_3layer_load import gru3_load
# from RNNMdls.gru_4layer_load import gru4_load
#
# from RNNMdls.gru_2layer_demo import gru2_demo

from label_generation import label_generator
from data_partition import data_partition
from dataDownload import data_downloader_multi
from featureExtraction import feature_extractor_multi
from data_process import normTrainTest


# updates.YYYYMMDD.HHMM.gz
############################ Test ############################
## Test in real-time
def test_realTime(ALGOs='BLS'):
    print("Choose collection site: RIPE or RouteViews")
    site = input('Collection site: ')
    if site == '':
        site = 'RIPE'

    if site == 'RIPE':
        time_interval = 330  # 5*60 add 30 sec because there is delay for ripe and routeviews.
    elif site == 'RouteViews':
        time_interval = 930  # 15*60 add 30 sec because there is delay for ripe and routeviews.
    else:
        print("Name of the collection site is incorrect.")
        exit()

    while True:
        year, month, day, hour, minute = time_locator_single(site)

        # print("Processing BGP update message: updates.%s%s%s.%s%s.gz"%(year,month,day,hour,minute))

        # data_date is used for data_link in Function data_downloader().
        update_message_file, data_date = updateMessageName(year, month, day, hour, minute)
        print('=> >>>>>>>>>> > > > > > ', 'Processing update_message_file:', update_message_file, '\n')

        data_downloader_single(update_message_file, data_date, site)
        file_name = feature_extractor_single(site)  # file_name not use

        if ALGOs == 'BLS':
            ### BLS
            subprocess_cmd("cd BLS_SFU_CNL_V101/; \
							python3 -W ignore BLS_demo.py ")
        elif ALGOs == 'GRU':
            ### GRU
            # gru2_demo()
            pass

        time.sleep(time_interval)


## Test manually
def test_random(ALGOs='GRU'):
    print("Choose collection site: RIPE or RouteViews")
    site = input('Collection site: ')
    if site == '':
        site = 'RIPE'

    if site == 'RIPE':
        pass
    elif site == 'RouteViews':
        pass
    else:
        print("Name of the collection site is incorrect.")
        exit()

    print("Date and time format: YYYY-MM-DD, HH:MM")
    year = input('year: ')
    if year == '':
        year = '2015'
    month = input('month: ')
    if month == '':
        month = '01'
    day = input('day: ')
    if day == '':
        day = '01'
    hour = input('hour: ')
    if hour == '':
        hour = '01'
    minute = input('minute: ')
    if minute == '':
        minute = '00'
    ############################

    # data_date is used for data_link in Function data_downloader().
    update_message_file, data_date = updateMessageName(year, month, day, hour, minute)
    print('update_message_file:', update_message_file)

    data_downloader_single(update_message_file, data_date, site)
    file_name = feature_extractor_single(site)  # file_name not use

    if ALGOs == 'BLS':
        ### BLS
        subprocess_cmd("cd BLS_SFU_CNL_V101/; \
						python3 -W ignore BLS_demo.py ")  # -W = ignore warnings
    elif ALGOs == 'GRU':
        ### GRU
        gru2_demo()


### Experiment for anomalous event
def expBGP(ALGOs='GRU'):
    # start_date = '20030123'
    # end_date = '20030127'
    # start_date_anomaly = '20030125'
    # end_date_anomaly = '20030125'
    # start_time_anomaly = '0531' #869 ones
    # end_time_anomaly = '1959'
    # site = 'RIPE'
    # cut_pct = '64'
    # rnn_seq = 10
    # output_file_list = ["DUMP_20030123_out.txt","DUMP_20030124_out.txt","DUMP_20030125_out.txt",
    # 					"DUMP_20030126_out.txt","DUMP_20030127_out.txt"]

    # Load input settings (dict)
    with open('input_exp.txt', 'r') as f:
        input_exp = f.read()
        input_exp = eval(input_exp)

    site = 'site'
    start_date = 'start_date'
    end_date = 'end_date'
    start_date_anomaly = 'start_date_anomaly'
    end_date_anomaly = 'end_date_anomaly'
    start_time_anomaly = 'start_time_anomaly'  # 869 ones
    end_time_anomaly = 'end_time_anomaly'
    cut_pct = 'cut_pct'
    rnn_seq = 'rnn_seq'

    for input_exp_key in input_exp:  # input_exp is a dictionary
        if site == input_exp_key:
            site = input_exp[input_exp_key]
        elif start_date == input_exp_key:
            start_date = input_exp[input_exp_key]
        elif end_date == input_exp_key:
            end_date = input_exp[input_exp_key]
        elif start_date_anomaly == input_exp_key:
            start_date_anomaly = input_exp[input_exp_key]
        elif end_date_anomaly == input_exp_key:
            end_date_anomaly = input_exp[input_exp_key]
        elif start_time_anomaly == input_exp_key:
            start_time_anomaly = input_exp[input_exp_key]
        elif end_time_anomaly == input_exp_key:
            end_time_anomaly = input_exp[input_exp_key]
        elif cut_pct == input_exp_key:
            cut_pct = input_exp[input_exp_key]
        elif rnn_seq == input_exp_key:
            rnn_seq = input_exp[input_exp_key]
        else:
            print("Error...")
            exit()
    print("--------------------Loading settings successfully-------------")

    collector_ripe = 'rrc04'
    data_downloader_multi(start_date, end_date, site, collector_ripe)
    output_file_list = feature_extractor_multi(start_date, end_date, site)
    labels = label_generator(start_date_anomaly, end_date_anomaly, start_time_anomaly, end_time_anomaly, site,
                             output_file_list)
    data_partition(cut_pct, site, output_file_list, labels, rnn_seq)
    normTrainTest(cut_pct, site)

    print("--------------------Experiment-Begin--------------------------")
    subprocess_cmd("cp ./data_split/train_%s_%s_n.csv ./data_split/test_%s_%s_n.csv ./RNN_Running_Code/RNN_Run/dataset/ ; \
					cd RNN_Running_Code/RNN_Run/dataset/; \
					mv train_%s_%s_n.csv train.csv; mv test_%s_%s_n.csv test.csv; \
					cd ..; cd ..; \
					chmod +x integrate_run.sh; sh ./integrate_run.sh ; \
					cd RNN_Run/; sh ./collect.sh; \
					cp -r res_acc res_run ../data_representation/ ; \
					cd .. ; cd data_representation/ ; \
					python3 TableGenerator.py; " \
                   % (cut_pct, site, cut_pct, site, cut_pct, site, cut_pct, site))

    print("--------------------Experiment-end----------------------------")
    subprocess_cmd("mv ./RNN_Running_Code/data_representation/data_representation_table.csv ./STAT/ ; \
					mv ./STAT/data_representation_table.csv ./STAT/results_%s_%s.csv" \
                   % (cut_pct, site))

    # Remove generated folders
    subprocess_cmd("cd RNN_Running_Code/RNN_Run/; \
					rm -rf ./experiment/ ./res_acc/ ./res_run/ ./tmp/")


### SMC2020 Testing
# def smc2020_slammer_ripe():
# 	gru4_load(5, './data_historical', './RNNMdls')


############################ Running ############################
if __name__ == '__main__':
    print("Test or Experiment?")
    mode_te = input('Mode: ')
    if mode_te == 'Test':
        print("Input mode: testRandom or testOnline?")
        inputMode = input('Mode: ')
        if inputMode == 'testRandom':
            test_random('BLS')
        elif inputMode == 'testOnline':
            test_realTime('BLS')
        elif inputMode == '':
            test_random('BLS')
        else:
            print("Mode name is incorrect.")
            exit()
    elif mode_te == 'Experiment':
        expBGP()
    else:
        print("Please re-enter.")
        exit()

# ripe:
# http://data.ris.ripe.net/rrc04/
# routeviews:
# http://archive.routeviews.org/bgpdata/
