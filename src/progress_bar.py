"""
    @author Zhida Li
    @email zhidal@sfu.ca
    @date Apr. 27, 2020
    @version: 1.1.0
    @description:
                This module contains the function for generation of the progress bar in terminal.

    @copyright Copyright (c) Apr. 27, 2020
        All Rights Reserved

    This Python code (versions 3.6 and newer)
"""

# ==============================================
# progress_bar()
# ==============================================

# Import the built-in libraries
import time

from progress import progress


def progress_bar(time_sleep=0.01, status_p='Running'):
    total = 100
    i = 0
    while i < total:
        i += 1
        progress(i, total, status=status_p)
        time.sleep(time_sleep)
