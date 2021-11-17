from machine import Timer, Pin
from .wifi_reset import delete_wifi
import urequests
from . import wifimanager 
from .ota_utils import download_and_install_update_if_available
from .tb_client import  fetching_data,connect_subscribe,check_subscription
from .play_audio import play_audio, Player
from .time_utils import time_set
from .led import blink
from time import sleep

 

def boot():
    blink.RED_color()
    delete_wifi()
    player = Player (busy_pin=Pin(4))
    player.play(1,0)
    # print(player.playing())
    while player.playing():
        sleep(0.1)

    
    wlan = wifimanager.get_connection()
    

    if wlan is None:
        print("Could not initialize the network connection.")
        try:
            timer_0 = Timer(0)
            timer_0.init(period=2000, mode=Timer.PERIODIC, callback=play_audio)
        except OSError as e:
            print("printing",str(e))
            print("Data not found and You're not connected to the internet")
                #only work when esp32 is connected to internet and thingsboard
     
    else:    
        #it will sync time with ntp server through internet
        try:
            response = urequests.get("http://clients3.google.com/generate_204")
            print(response.status_code)
            if response.status_code == 204:  
                time_set()
                print("Time set")
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
            print("Exception occured in connect_subscribe", str(e))

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
            timer_1.init(period=60000, mode=Timer.PERIODIC, callback=check_subscription)
        except OSError as e:
            print(str(e))
            print("Failed to connect with Internet or thingsboard server")

        try:
            timer_2 = Timer(2)
            timer_2.init(period=4000, mode=Timer.PERIODIC, callback=fetching_data)
        except OSError as e:
            print(str(e))
            print("Failed to receive time table this time")
    
