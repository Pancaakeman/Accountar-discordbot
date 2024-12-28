import datetime

#print(datetime.datetime.now())
#print(datetime.date.today())


#date = datetime.date.today()
#current =datetime.datetime.now()
#reset = datetime

#reset_time = datetime.datetime(year = current.year, month = current.month, day= current.day)
#print(reset_time)


def time_check():
    current = datetime.datetime.now()
    reset_time = datetime.datetime(year = current.year, month = current.month, day= current.day,hour=00,minute=00,second=00)
    #time_left = reset_time - current
    if current > reset_time:
        print("can collect")
    else: 
        print("cant collect")
    #print(time_left)
    
time_check()