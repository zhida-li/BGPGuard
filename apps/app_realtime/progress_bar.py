# Generate the progress bar
# Call function progress.py
# Apr. 27, 2020
import time
from progress import progress


def progress_bar(time_sleep=0.01, status_p='Running'):
    total = 100
    i = 0
    while i < total:
        i += 1
        progress(i, total, status=status_p)
        time.sleep(time_sleep)
