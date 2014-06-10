import time

#prompt the user for show name.
#show name should be as precise as possible with episode or season number.
#for example 'chuck season 1'
try:
    user_input = input('Please enter the show name you want to schedule a download for:')
    file = open("showname.txt", "w")
    file.write("Show Name : "+user_input)
    file.close()
    print('Input saved sucessfully. Download will start at 4 AM.')
    time.sleep(10)
except Exception as e:
    print('Some error saving the show name, please try again.')
    
