from secrets import *
from serial import *
import mqtt_CBR
import time
import machine

mqttBroker = '10.0.0.125'
topicSub = 'ESP/listen'
topicPub = 'ESP/tell'
clientID = 'Jacob_Suely_ESP'

def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    blink()
    time.sleep(0.5)
    blink()

mqtt_CBR.connect_wifi(Home_WiFi)
client = mqtt_CBR.mqtt_client(clientID, mqttBroker, whenCalled)

def main():
    s = serial_comm(115200)
    s.abort()
    while True:
        if (s.any()):
            command = s.read()
            client.publish(topicPub, command)
            break
        time.sleep(0.5)
