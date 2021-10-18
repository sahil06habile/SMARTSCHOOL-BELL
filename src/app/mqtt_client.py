import ujson as json
import time
from machine import Pin
from utime import sleep
from .http_client import HttpClient
from uthingsboard.client import TBDeviceMqttClient
from .play_audio  import get_curr_time
from .wifimanager import wlan_sta
from .led import blink

def save_mqtt(result):
    payload = json.dumps(result)
    f = open("/mqtt-time-table.json", "w")
    f.write(payload)
    f.close()



global result
#Get Data from MQTT
def connect_subscribe():
        global client
        f=open('token.json','r')
        TOKEN = json.loads(f.read())
        f.close()
        print((TOKEN['token']))
        client = TBDeviceMqttClient('dev-iot.habilelabs.io', access_token=(TOKEN['token']))
        while not wlan_sta.isconnected(): pass
        def on_attributes_change(result):
           print(result)
           save_mqtt(result)
        client.connect()
        print(client._is_connected)
        print("Conncted via mqtt")
        client.subscribe_to_all_attributes(callback=on_attributes_change)
        print("Subscribed")
        return client   

def check_subscription(timer_1):
        connect_subscribe()


def save_mqtt(result):
    payload = json.dumps(result)
    f = open("/mqtt-time-table.json", "w")
    f.write(payload)
    f.close()

		
def fetching_data(timer_2):
        while True:
            try:
                print("getting Data")
                print("mqtt is" ,client._is_connected)
                new_message = client.check_msg()
                print("CHECK mSG iS",client.check_msg())
                if new_message != 'None':
                    print("Data saved")
                    # led = Pin(2,Pin.OUT)
                    # led.on()
                    blink.RED_color()
                    sleep(1)
                    blink.BLUE_color()
                    sleep(1)
                    break
                else:
                    print("No new data found for bell")
                    led=Pin(34,Pin.OUT)
                    led.on()
                    sleep(1)
                    led.off()
                    sleep(1)
            except OSError as e:
                print("Exception occured in fetching data", str(e))







