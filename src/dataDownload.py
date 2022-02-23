"""
    @author Zhida Li
    @email zhidal@sfu.ca
    @date May. 04, 2020
    @version: 1.1.0
    @description:
                Download update messages from RIPE or RouteViews

    @copyright Copyright (c) May. 04, 2020
        All Rights Reserved

    This Python code (versions 3.6 and newer)
"""

# ==============================================
# updateMessageName(), data_downloader_single(), data_downloader_multi()
# ==============================================
# Last modified: Feb. 19, 2022

# Import the built-in libraries
import os
import sys

# Import customized libraries
sys.path.append('./src')
from progress_bar import progress_bar
from subprocess_cmd import subprocess_cmd
from time_tracker import time_tracker_multi


# Name of the update_message_file generation
def updateMessageName(year, month, day, hour, minute):
    # updates.YYYYMMDD.HHMM.gz,  minute: 5 minutes interval

    data_date = "%s.%s" % (year, month)  # used for data_link in Function data_downloader(). 

    # Code below also works
    # update_message_file = 'updates.' + str(year) + str(month)+ str(day)+ '.'+ str(hour)+ str(minute)+'.'+'gz'
    update_message_file = "updates.%s%s%s.%s%s" % (year, month, day, hour, minute)
    return update_message_file, data_date  # these two outputs are string


# Download specific file from RIPE or RouteViews
# rcc04: Geneva
def data_downloader_single(update_message_file, data_date, site, collector_ripe='rrc04',
                           collector_routeviews='route-views2'):
    data_file = update_message_file

    if site == 'RIPE':
        data_link = "https://data.ris.ripe.net/%s/%s/%s.gz" % (collector_ripe, data_date, data_file)

        # Update message files will be downloaded in "data_ripe" folder: --directory-prefix
        subprocess_cmd("chmod -R 777 ./src/;\
                        cd src/; wget -np --accept=gz %s \
                        --directory-prefix=data_ripe ; \
                        cd data_ripe ; \
                        chmod +x name-change-script.sh ;\
                        sh ./name-change-script.sh ; \
                        echo '=> >>>>>>>>>> > > > > > Extension changed (gz to Z)' " % (data_link))

        subprocess_cmd("cd src/; cd data_ripe ; \
                        chmod +x zebra-script.sh ;\
                        sh ./zebra-script.sh")

        progress_bar(time_sleep=0.02, status_p='Converting')

        subprocess_cmd("echo ' '; \
                        echo '=> >>>>>>>>>> > > > > > DUMP generated (MRT to ASCII)' ")

        # Move .Z file, then remove it
        subprocess_cmd("cd src/; mv ./data_ripe/%s.Z ./data_ripe/temp/; \
                        rm ./data_ripe/DUMPER; \
                        rm ./data_ripe/temp/%s.Z" % (data_file, data_file))

    # collector_routeviews is not finished (only use 'route-views2' now)
    elif site == 'RouteViews':
        data_link2 = "https://archive.routeviews.org/bgpdata/%s/UPDATES/%s.bz2" % (data_date, data_file)

        # Update message files will be downloaded in "data_routeviews" folder: --directory-prefix
        subprocess_cmd("wget -np --accept=bz2 %s \
                        --directory-prefix=data_routeviews ; \
                        cd data_routeviews ;" % (data_link2))

        subprocess_cmd("cd data_routeviews ; \
                        chmod +x zebra-script.sh ;\
                        sh ./zebra-script.sh ; \
                        echo '=> >>>>>>>>>> > > > > > Decompressed bz2' ")

        progress_bar(time_sleep=0.02, status_p='Converting')

        subprocess_cmd("echo ' '; \
                        echo '=> >>>>>>>>>> > > > > > DUMP generated (MRT to ASCII)' ")

        # Move Decompressed file, then remove it
        subprocess_cmd("mv ./data_routeviews/%s ./data_routeviews/temp/ ; \
                        rm ./data_routeviews/DUMPER; \
                        rm ./data_routeviews/temp/%s" % (data_file, data_file))
    else:
        print("Wrong name")
        exit()


# Multiple files (days)
def data_downloader_multi(start_date, end_date, site, collector_ripe='rrc04', collector_routeviews='route-views2'):
    # updates.YYYYMMDD.HHMM.gz
    # data_date = "%s.%s" % (year, month)
    # update_message_file = "updates.%s%s%s.%s%s" % (year, month, day, hour, minute)
    date_list = time_tracker_multi(start_date, end_date)
    print(date_list)

    # RIPE
    if site == 'RIPE':
        for date_i in date_list:
            # Create folders for each day
            date_i_folder = './data_ripe/%s' % date_i
            if not os.path.exists(date_i_folder):
                os.makedirs(date_i_folder)
                print("\n RIPE => >>>>>>>>>> Folder %s has been created." % (date_i))

            # Move dump parser to each folder
            subprocess_cmd("cd data_ripe/ ; \
                            cp name-change-script.sh zebra-dump-parser-modified.pl zebra-script.sh ./%s ; \
                            cd %s/ " % (date_i, date_i))

            # Download
            year = date_i[0:4]
            month = date_i[4:6]
            data_date = "%s.%s" % (year, month)

            data_link = "https://data.ris.ripe.net/%s/%s/" % (collector_ripe, data_date)
            data_file = 'updates.%s.*.gz' % date_i
            data_file_rm = 'updates.%s.*.Z' % date_i

            subprocess_cmd("cd data_ripe/%s/ ; \
                            wget -e robots=off -r -np -nd -A '%s' %s ;" % (date_i, data_file, data_link))

            # Generate DUMP using Zebra
            subprocess_cmd("cd data_ripe/%s/ ; \
                            chmod +x name-change-script.sh ; sh ./name-change-script.sh ; \
                            echo '=> >>>>>>>>>> > > > > > Extension changed (gz to Z)' ;\
                            chmod +x zebra-script.sh ; sh ./zebra-script.sh ; \
                            mv DUMP DUMP_%s" % (date_i, date_i))

            progress_bar(time_sleep=0.02, status_p='Converting')

            subprocess_cmd("echo ' '; \
                            echo '=> >>>>>>>>>> > > > > > DUMP generated (MRT to ASCII)' ")

            # Remove .Z file
            subprocess_cmd("rm ./data_ripe/%s/%s" % (date_i, data_file_rm))

    # RouteViews
    # collector_routeviews is not finished (only use 'route-views2' now)
    elif site == 'RouteViews':
        for date_i in date_list:
            # Create folders for each day
            date_i_folder = './data_routeviews/%s' % date_i
            if not os.path.exists(date_i_folder):
                os.makedirs(date_i_folder)
                print("\n RouteViews => >>>>>>>>>> Folder %s has been created." % (date_i))

            # Move dump parser to each folder
            subprocess_cmd("cd data_routeviews/ ; \
                            cp zebra-dump-parser-modified.pl zebra-script.sh ./%s ; \
                            cd %s/ " % (date_i, date_i))

            # Download
            year = date_i[0:4]
            month = date_i[4:6]
            data_date = "%s.%s" % (year, month)

            data_link = "https://archive.routeviews.org/bgpdata/%s/UPDATES/" % (data_date)
            data_file = 'updates.%s.*.bz2' % date_i
            data_file_rm = 'updates.%s.*' % date_i

            subprocess_cmd("cd data_routeviews/%s/ ; \
                            wget -e robots=off -r -np -nd -A '%s' %s ;" % (date_i, data_file, data_link))

            # Generate DUMP using Zebra
            subprocess_cmd("cd data_routeviews/%s/ ; \
                            chmod +x zebra-script.sh ; sh ./zebra-script.sh ; \
                            echo '=> >>>>>>>>>> > > > > > Decompressed bz2' ; \
                            mv DUMP DUMP_%s" % (date_i, date_i))

            progress_bar(time_sleep=0.02, status_p='Converting')

            subprocess_cmd("echo ' '; \
                            echo '=> >>>>>>>>>> > > > > > DUMP generated (MRT to ASCII)' ")

            # Remove .Z file
            subprocess_cmd("rm ./data_routeviews/%s/%s" % (date_i, data_file_rm))
    else:
        print("Wrong name")
        exit()
