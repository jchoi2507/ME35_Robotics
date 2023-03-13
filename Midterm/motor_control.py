'''

motor_control.py

- RP2040 script
- Inputs angle values from a JSON file
- Sends angle values to move motors over MQTT

'''

import time
import math
import json
import mqtt_CBR
from secrets import *
from machine import Pin, ADC

def parseAngles():
    file = open("motor_angles.txt")
    data = json.load(file)
    theta1 = data[0]
    theta2 = data[1]
    file.close()
    return theta1, theta2

def whenCalled(topic, msg):
    time.sleep(0.5)

def sendAngles(theta1, theta2):
    # MQTT connection
    
    mqttBroker = "10.0.0.125"
    topicPub = "angles"
    clientID = "Jacob"
    mqtt_CBR.connect_wifi(Home_WiFi)
    client = mqtt_CBR.mqtt_client(clientID, mqttBroker, whenCalled)
    
    # Sending formatted angles
    counter = 0
    for i in theta1:
        angle1 = i
        angle2 = theta2[counter]
        
        msg = "(" + str(angle1) + "," + str(angle2) + ")"
    
        client.publish(topicPub, msg)
        counter += 1
        time.sleep(5)

def main():
    theta1, theta2 = parseAngles()
    sendAngles(theta1, theta2)
