'''

ESP8266_CrazyCar.py

MicroPython script loaded onto ESP8266

1) Publishes a command to an MQTT topic

'''

from secrets import *
from serial import *
import time

mqttBroker = '10.0.0.125'
topicSub = 'ESP/listen'
topicPub = 'ESP/tell'
clientID = 'Jacob_Suely_ESP'

def whenCalled(topic, msg):
    time.sleep(0.5)

import mqtt_CBR
mqtt_CBR.connect_wifi(Home_WiFi)
client = mqtt_CBR.mqtt_client(clientID, mqttBroker, whenCalled)
client.publish(topicPub, "0")

