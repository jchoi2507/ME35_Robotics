'''

ESP8266_boot.py

This script is included in the ESP8266 boot.py file,
which connects the ESP8266 to the broker
at every boot sequence of the ESP8266.


'''

import mqtt_CBR
import time
from secrets import *

mqttBroker = '10.0.0.125'
topicSub = 'ESP/listen'
topicPub = 'ESP/tell'
clientID = 'Jacob_Suely_ESP'

def callback():
    time.sleep(0.1)

mqtt_CBR.connect_wifi(Home_WiFi)
client = mqtt_CBR.mqtt_client(clientID, mqttBroker, callback())

