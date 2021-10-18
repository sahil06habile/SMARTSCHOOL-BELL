from app import wifimanager
from machine import Pin, reset 
from time import sleep
import os 
from .led import blink

def delete_file():
    try:
        wifimanager.start()
    except OSError:
        print("wifi.dat file not available")

def delete_wifi():
    push_button = Pin(15, Pin.IN)
    if push_button.value():
        for i in range(0, 6):     
            logic_value = push_button.value()
            if i<4 and logic_value ==1:
                i = i+logic_value
                print(i)
            elif i==4 and logic_value == 1:
                blink.YELLOW_color()
                delete_file()
                break
            elif i<4 and logic_value ==0:
                break
            sleep(1)
    else:
        print("Program Running")