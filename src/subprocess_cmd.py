"""
    @author Zhida Li
    @email zhidal@sfu.ca
    @date May. 01, 2020
    @version: 1.1.0
    @description:
                This module contains the function for execution of the bash command.

    @copyright Copyright (c) May. 01, 2020
        All Rights Reserved

    This Python code (versions 3.6 and newer)
"""

# ==============================================
# subprocess_cmd()
# ==============================================

# Import the built-in libraries
import subprocess


# The code below also works, generate same output when using function subprocess_cmd().
# def subprocess_cmd1(command):
#     process = subprocess.Popen(command,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
#     proc_stdout = process.communicate()[0].decode('utf-8').strip()
#     print(proc_stdout)

def subprocess_cmd(command):
    output = subprocess.check_output(command, shell=True).decode('utf-8')  # In Python 2.7,remove decode('utf-8')
    print(output)
