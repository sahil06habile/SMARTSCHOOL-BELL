from machine import Timer, reset
from .wifi_reset import delete_wifi
from . import wifimanager 
from .ota_utils import download_and_install_update_if_available
from .tb_client import  fetching_data,connect_subscribe,check_subscription
from .play_audio import play_audio
from .time_utils import time_set



def boot():
    delete_wifi()
    wlan = wifimanager.get_connection()
    if wlan is None:
        print("Could not initialize the network connection.")
        try:
            timer_0 = Timer(0)
            timer_0.init(period=2000, mode=Timer.PERIODIC, callback=play_audio)
        except OSError as e:
            print(str(e))
            print("Data not found and You're not connected to the internet")
                #only work when esp32 is connected to internet and thingsboard
        #check tb_client.py in app dir and correct server details
        try:
            timer_1 = Timer(1)
            timer_1.init(period=120000, mode=Timer.PERIODIC, callback=check_subscription)
        except OSError as e:
            print(str(e))
            print("Failed to connect with Internet or thingsboard server")

        try:
            timer_2 = Timer(2)
            timer_2.init(period=4000, mode=Timer.PERIODIC, callback=fetching_data)
        except OSError as e:
            print(str(e))
            print("Failed to receive time table this time")
    else:    
        #it will sync time with ntp server through internet
        try:
            time_set()
        except OSError as e:
            print(str(e))
            print("You're not connected to internet")

        # it will check if update is available and then download ,install and reboot
        try:
          download_and_install_update_if_available()
        except:
          print("Something went wrong while update")  
        try:
            connect_subscribe()
        except OSError as e:
            print("Exception occured in send_mqtt", str(e))

        #only work when data is saved in time-table.json at root dir
        try:
            timer_0 = Timer(0)
            timer_0.init(period=2000, mode=Timer.PERIODIC, callback=play_audio)
        except OSError as e:
            print(str(e))
            print("Data not found and You're not connected to the internet")



        #only work when esp32 is connected to internet and thingsboard
        #check tb_client.py in app dir and correct server details
        try:
            timer_1 = Timer(1)
            timer_1.init(period=120000, mode=Timer.PERIODIC, callback=check_subscription)
        except OSError as e:
            print(str(e))
            print("Failed to connect with Internet or thingsboard server")

        try:
            timer_2 = Timer(2)
            timer_2.init(period=4000, mode=Timer.PERIODIC, callback=fetching_data)
        except OSError as e:
            print(str(e))
            print("Failed to receive time table this time")
    
