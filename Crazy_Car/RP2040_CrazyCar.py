'''

RP2040_CrazyCar.py

MicroPython script loaded onto RP2040.

1) main() executes once correct Airtable field is inputted
2) Waits for a physical tap onto the RP2040 to then open a
line of serial communication to the ESP8266.

'''

# If edits to this file aren't updating properly,
# soft reset w/ CTRL + D

import time
from serial import *
from lsm6dsox import LSM6DSOX
from machine import Pin, I2C

accel_x_threshold = 0.5 # Minimum x-value accelorometer reading to open
                        # serial communication w/ ESP8266

lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))

code = '''
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
'''

# accelListen() waits for threshold accelorometer reading to be reached
def accelListen():
    keepLooping = True
    while (keepLooping):
        accel_data_arr = lsm.read_accel() # read accelerometer data into an array
        accel_data_x = accel_data_arr[0] # interested in changes in x position only
        print(accel_data_x)
        
        if (accel_data_x > accel_x_threshold):
            keepLooping = False
        time.sleep(1)

# startESP8266() actually serially communicates to the ESP8266
def startESP8266(code):
    print("Opening serial line to ESP8266...")
    s = serial_comm(115200)
    s.abort()

    s.send_code(code) # Sending code to ESP8266
    
    while True:
        if s.any():
            text = s.readln()
            print(text, end='')
        time.sleep(0.1)

# main()
def main():
    accelListen()
    startESP8266(code)
    
