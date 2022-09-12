import datetime
import time


# Driver takes care of all time stamp conversions
# Used to make sure Twarc is getting the newest reports only

def fetch_date():

    date= datetime.datetime.today() 
    date=date.strftime('%m/%d/%Y')
 
    return str(date)

def regular_datetime():
    import datetime
    date= datetime.datetime.today() 
    date=date.strftime('%Y-%m-%d %H:%M:%S')
    return date


def fetch_time(): # Epoch timestamp

    timestamp=time.time()

    return timestamp 


def convert_epoch_to_datetime(timestamp):
    return time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(timestamp))

def convert_created_at(created_at): # Function to convert twitter created_at to python timestamp
 
    import datetime
    datetime_stamp=datetime.datetime.strptime(created_at,"%Y-%m-%dT%H:%M:%S.%fZ")
    return datetime_stamp

def convert_to_epoch(datetime_stamp): # Function to convert python timestamp to unix timestamp
     import datetime
     epoch=datetime.datetime.strptime(datetime_stamp,"%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
     return epoch

def datetime_to_epoch(input): # Epoch timestamp

    input=str(input)
    import datetime
    epoch=datetime.datetime.strptime(input,"%Y-%m-%d %H:%M:%S").timestamp()
    return epoch