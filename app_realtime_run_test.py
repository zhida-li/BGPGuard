# Run: python3 main.py
# May. 07, 2020
import sys
import time
sys.path.append('./apps/app_realtime/')
from dataDownload import data_downloader_single
from dataDownload import updateMessageName
from featureExtraction import feature_extractor_single
from time_locator import time_locator_single

sys.path.append('./apps/app_realtime/BLS_SFU_CNL_V101')
from BLS_SFU_CNL_V101.BLS_demo import bls_demo


# updates.YYYYMMDD.HHMM.gz
# Real-time detection
def app_realtime(ALGOs='BLS'):
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
        print('=> >>>>>>>>>> > > > > > ',
              'Processing update_message_file:', update_message_file,
              ' < < < < < <<<<<<<<<< <= \n')
        data_downloader_single(update_message_file, data_date, site)
        file_name = feature_extractor_single(site)  # file_name not use

        if ALGOs == 'BLS':
            ### BLS
            predicted_list, test_hour, test_min, web_results = bls_demo()
            predicted_list, test_hour_list, test_min_list = predicted_list, test_hour.tolist(), test_min.tolist()
            print("predicted", predicted_list)
            print("test_hour", test_hour_list)
            print("test_min", test_min_list)
            print("web_results", web_results)
        elif ALGOs == 'GRU':
            ### GRU
            # gru2_demo()
            print("Please re-enter.")
            exit()

        time.sleep(time_interval)

############################ Running ############################
app_realtime()


# ripe:
# http://data.ris.ripe.net/rrc04/
# routeviews:
# http://archive.routeviews.org/bgpdata/
