"""
    @author Zhida Li
    @email zhidal@sfu.ca
    @date May. 01, 2020
    @version: 1.1.0
    @description:
                Generate the matrix using BGP C# tool.

    @copyright Copyright (c) May. 01, 2020
        All Rights Reserved

    This Python code (versions 3.6 and newer)
"""

# ==============================================
# feature_extractor_single(), feature_extractor_multi
# ==============================================
# Last modified: Feb. 19, 2022

# Import the built-in libraries
# import time

# Import customized libraries
from progress_bar import progress_bar
from subprocess_cmd import subprocess_cmd
from time_tracker import time_tracker_multi


# Matrix generation
# Input: DUMP
# Output: DUMP_out.txt
def feature_extractor_single(site, file_name='DUMP'):
    # Update message files will be downloaded in "data_ripe" or "data_routeviews" folder
    # line 19: &> ConsoleApplication1.out ; \
    # Move DUMP
    if site == 'RIPE':
        subprocess_cmd("cd src/; \
                        mv ./data_ripe/%s ./CSharp_Tool_BGP/ConsoleApplication1/bin/Release/ ; \
                        cd CSharp_Tool_BGP/ConsoleApplication1/bin/Release/ ; \
                        mono ConsoleApplication1.exe >/dev/null ; \
                        rm %s ; \
                        cd ..; cd ..; cd ..; cd ..; " % (file_name, file_name))
    elif site == 'RouteViews':
        subprocess_cmd("cd src/; \
                        mv ./data_routeviews/%s ./CSharp_Tool_BGP/ConsoleApplication1/bin/Release/ ; \
                        cd CSharp_Tool_BGP/ConsoleApplication1/bin/Release/ ; \
                        mono ConsoleApplication1.exe >/dev/null ; \
                        rm %s ; \
                        cd ..; cd ..; cd ..; cd ..; " % (file_name, file_name))
    else:
        print("Wrong name")
        exit()

    progress_bar(time_sleep=0.03, status_p='Generating')

    subprocess_cmd("echo ' '; \
                    echo '=> >>>>>>>>>> > > > > > Matrix generated (txt)' ; \
                    echo 'Current Path:'; pwd ")

    subprocess_cmd(" echo '+============================+';\
                    echo '| Data download     === done |';\
                    echo '| MRT to ASCII      === done |';\
                    echo '| Matrix generation === done |';\
                    echo '| Next step:                 |';\
                    echo '|        Classification      |';\
                    echo '+============================+';\
                    echo ' ' ")

    output_file = "%s_out.txt" % file_name

    # Move output_file
    subprocess_cmd("cd src/; mv ./CSharp_Tool_BGP/ConsoleApplication1/bin/Release/%s \
                        ./data_test/" % output_file)

    return output_file  # output is string


# Move DUMP file to C# tool, then, move DUMP_out.txt to data_test folder
def feature_extractor_multi(start_date, end_date, site):
    # Update message files will be downloaded in "data_ripe" or "data_routeviews" folder
    # line 19: &> ConsoleApplication1.out ; \

    date_list = time_tracker_multi(start_date, end_date)
    # print(date_list)
    if site == 'RIPE':
        output_file_list = []
        for date_i in date_list:
            file_name = 'DUMP_%s' % date_i
            subprocess_cmd("cd src/; \
                            mv ./data_ripe/%s/%s ./CSharp_Tool_BGP/ConsoleApplication1/bin/Release/ ; \
                            cd CSharp_Tool_BGP/ConsoleApplication1/bin/Release/ ; \
                            mv %s DUMP ; \
                            mono ConsoleApplication1.exe >/dev/null ; \
                            mv DUMP_out.txt %s_out.txt ; \
                            rm DUMP ; \
                            cd ..; cd ..; cd ..; cd ..; " % (date_i, file_name, file_name, file_name))

            progress_bar(time_sleep=0.03, status_p='Generating')

            subprocess_cmd("echo ' '; \
                            echo '=> >>>>>>>>>> > > > > > Matrix generated (txt)' ; \
                            echo 'Current Path:'; pwd ")

            subprocess_cmd(" echo '+============================+';\
                            echo '| Data download     === done |';\
                            echo '| MRT to ASCII      === done |';\
                            echo '| Matrix generation === done |';\
                            echo '| Next step:                 |';\
                            echo '|        Classification      |';\
                            echo '+============================+';\
                            echo ' ' ")

            output_file = "%s_out.txt" % file_name
            output_file_list.append(output_file)

            # Move output_file
            subprocess_cmd("cd src/; mv ./CSharp_Tool_BGP/ConsoleApplication1/bin/Release/%s \
                                ./data_split/" % output_file)

    elif site == 'RouteViews':
        output_file_list = []
        for date_i in date_list:
            file_name = 'DUMP_%s' % date_i
            subprocess_cmd("cd src/; \
                            mv ./data_routeviews/%s/%s ./CSharp_Tool_BGP/ConsoleApplication1/bin/Release/ ; \
                            cd CSharp_Tool_BGP/ConsoleApplication1/bin/Release/ ; \
                            mv %s DUMP ; \
                            mono ConsoleApplication1.exe >/dev/null ; \
                            mv DUMP_out.txt %s_out.txt ; \
                            rm DUMP ; \
                            cd ..; cd ..; cd ..; cd ..; " % (date_i, file_name, file_name, file_name))

            progress_bar(time_sleep=0.03, status_p='Generating')

            subprocess_cmd("echo ' '; \
                            echo '=> >>>>>>>>>> > > > > > Matrix generated (txt)' ; \
                            echo 'Current Path:'; pwd ")

            subprocess_cmd(" echo '+============================+';\
                            echo '| Data download     === done |';\
                            echo '| MRT to ASCII      === done |';\
                            echo '| Matrix generation === done |';\
                            echo '| Next step:                 |';\
                            echo '|        Classification      |';\
                            echo '+============================+';\
                            echo ' ' ")

            output_file = "%s_out.txt" % file_name
            output_file_list.append(output_file)

            # Move output_file
            subprocess_cmd("cd src/; mv ./CSharp_Tool_BGP/ConsoleApplication1/bin/Release/%s \
                                ./data_split/" % output_file)
    else:
        print("Wrong name")
        exit()

    return output_file_list  # a list of output file, may be used to load for partition module
