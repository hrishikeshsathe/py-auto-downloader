import os
import time
import requests

try:
    time.sleep(30)
    
    #try to get a google page. if it timeouts then internet is not connected and exception is raised
    response = requests.get('http://74.125.228.100',timeout=5)
    
    #retrieve the current system time and check if its in between 4 AM and 5 AM (scheduled time for download)
    hours = time.localtime().tm_hour
    if hours == 19:
        os.startfile("D:\Aptana\workspace\Tutorials\py_scheduler.py") #start the scheduler
    
except Exception as e:
    #Shutdown the system if there is a problem connecting to the internet
    os.system('shutdown /s')