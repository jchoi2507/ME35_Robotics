'''

ESP8266_CrazyCar.py

MicroPython script loaded onto ESP8266

1) Publishes a command to an MQTT topic
Note: MQTT setup and connection is performed on boot, in ESP8266_boot.py

'''

from secrets import *
from serial import *
import mqtt_CBR
import time
import machine

mqttBroker = '10.0.0.125'
topicSub = 'ESP/listen'
topicPub = 'ESP/tell'
clientID = 'Jacob_Suely_ESP'

def main():
    s = serial_comm(115200)
    #s.abort()
    #while True:
    #    if (s.any()):
    #        print("DATA RECEIVED\n")
    #        command = s.read()2
    #        client.publish(topicPub, command)
    #        break
    time.sleep(0.5)

main()
