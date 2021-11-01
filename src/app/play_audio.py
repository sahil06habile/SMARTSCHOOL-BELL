import ujson as json
from utime import sleep
from machine import Pin
from .time_utils import time_get
from .dfplayer import Player

last_play_time = ""

player = Player(busy_pin=Pin(4))

ATTR_TYPE = "shared"



def get_curr_time():
    ds = time_get()
    date_time = ds.date_time()
    year, month, mday, weekday, hour, minute, second = date_time
    curr_time = "{}:{}".format(hour,minute)
    day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    curr_day = day_list[weekday]
    curr_date = "{}-{}-{}".format(mday,month,year)
    return curr_time, curr_day,curr_date

    
def get_time_table():
    try:
        f = open('mqtt-time-table.json','r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data
    except OSError as e:
        print('Exception occured', e)


def play_audio(timer_0):
    global last_play_time
    curr_time, curr_day,curr_date = get_curr_time()
    print('current time is ', curr_time, 'and day is: ',curr_day)
    time_table = get_time_table()
    sdata = time_table[ATTR_TYPE]
    if sdata['isPaused']== False:
        if curr_day in time_table[ATTR_TYPE]:
            data = time_table[ATTR_TYPE][curr_day]
            print("Data found for {}".format(curr_day))   
            for key,value in data.items():
                if last_play_time != curr_day + curr_time:
                    if data[key]['time'] == curr_time:
                        print("bell is ringing for {}".format(key),'and day is: ', curr_day)
                        for i in range(data[key]['count']):
                            if data[key]['isSpecialBell']:
                                player.play(0,1)
                                while player.playing():
                                    sleep(0.1)
                            else:
                                player.play(0,0)
                                while player.playing():
                                    sleep(0.1)
                        last_play_time = curr_day + curr_time
                else:
                    print("Bell already played for {}".format(last_play_time), 'and day is: ', curr_day)
                    return
    else:
        print("Bell is Paused")
        
    sdata = time_table[ATTR_TYPE]
    if sdata['isPaused']== False:
        if curr_date in time_table[ATTR_TYPE]:
            data = time_table[ATTR_TYPE][curr_date]
            print("Data found for {}".format(curr_date))   
            for key,value in data.items():
                if last_play_time != curr_date + curr_time:
                    if data[key]['time'] == curr_time:
                        print("bell is ringing for {}".format(key),'and date is: ', curr_date)
                        for i in range(data[key]['count']):
                            if data[key]['isSpecialBell']:
                                player.play(0,1)
                                while player.playing():
                                    sleep(0.1)
                            else:
                                player.play(0,0)
                                while player.playing():
                                    sleep(0.1)
                        last_play_time = curr_date + curr_time

        else:
            print("Bell already played for {}".format(last_play_time), 'and date is: ', curr_date)
            return
    else:
        print("Bell is Paused")