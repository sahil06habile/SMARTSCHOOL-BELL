import ujson as json
import time
from .http_client import HttpClient
from machine import Pin
import urequests
import gc
from utime import sleep
from uthingsboard.client import TBDeviceMqttClient
from .wifimanager import wlan_sta
from .led import blink




def get_status():
    try:
        f = open('token.json','r')
        DEVICEID = json.loads(f.read())
        f.close()
        requests = HttpClient()
        print("time sync")
        response = requests.get(url='https://dev-api.iot.habilelabs.io/smartbell/esp/{}'.format(DEVICEID['deviceId']),saveToFile=None)
        print("Latest time table is synced")
        return response.json()
    except OSError as e:
        print('exception occured in read deviceId, ',str(e))




def save_mqtt(reqresult):
    payload = json.dumps(reqresult)
    f = open("/mqtt-time-table.json", "w")
    f.write(payload)
    f.close()



global result
#Get Data from MQTT
def connect_subscribe():
        try:
            global client
            global result
            f=open('token.json','r')
            TOKEN = json.loads(f.read())
            f.close()
            print((TOKEN['token']))
            client = TBDeviceMqttClient('dev-iot.habilelabs.io', access_token=(TOKEN['token']))
            while not wlan_sta.isconnected(): pass
            client.connect()

            def on_attributes_change(result):
                val=result.get("isPaused",False)
                result["isPaused"]= val
                reqresult = { }
                reqresult["shared"]=result
                print(reqresult)
                save_mqtt(reqresult)
                if reqresult==None:
                    ("No new messages yet")
                else:
                    get_status()
                return reqresult 

            def on_data_changes(table):
                print(table)
                save_mqtt(table)

            
            print(client._is_connected)
            print("Conncted with MQTT Protocol")
            client.subscribe_to_all_attributes(callback=on_attributes_change)
            print("Subscribed")
            client.request_attributes(shared_keys=[],client_keys=[], callback=on_data_changes)
            client.wait_msg()
            return client   
        except OSError as e:
            print("Exception occured in connack and sub", str(e))


        

def check_subscription(timer_1):
    if wlan_sta.isconnected():
        connect_subscribe()
    else:
        print("WIFI is not available")



def save_mqtt(result):
    payload = json.dumps(result)
    f = open("/mqtt-time-table.json", "w")
    f.write(payload)
    f.close()

		
def fetching_data(timer_2):
    try:
        print("getting Data")
        print("mqtt is" ,client._is_connected)
        led = Pin(2,Pin.OUT)
        led.on()
        sleep(1)
        led.off()
        sleep(1)
        if wlan_sta.isconnected():
            if client._is_connected:
                try:
                    response = urequests.get("http://clients3.google.com/generate_204")
                    print(response.status_code)
                    if response.status_code == 204:  
                            print("online")
                            try:
                                client.check_msg()
                                sleep(1)  
                            except OSError as e:
                                print("Exception occureed in check_msg()",str(e))
                            print("Data saved")
                    else:
                        print("NO Internet")
                        try:
                            connect_subscribe()
                        except OSError as e:
                            print(str(e))
                    gc.collect()
                except OSError as e:
                    print(str(e))           
            else:
                print("client is not connected") 
                # try:      
                #     client.reconnect()
                #     print("Reconnected to client")
                # except OSError as e:
                #     print("Exception in reconnect", str(e))           
        else:
            print("WIFI is not available") 
    except OSError as e:
        print("Exception occured in line 81 tbclient", str(e))






