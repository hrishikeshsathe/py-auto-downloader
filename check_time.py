import os
import time

#retrieve the current system time and check if its in between 4 AM and 5 AM (scheduled time for download)
hours = time.localtime().tm_hour
if 4 <= hours <= 5:
    os.startfile("C:\py_scheduler.py") #start the scheduler
