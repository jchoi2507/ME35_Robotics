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

accel_x_threshold_pos = 0.5 # Minimum x-value accelorometer reading to open
                        # serial communication w/ ESP8266

accel_x_threshold_neg = -0.5

lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))

ESP_code_forward = '''
from secrets import *
from serial import *
import time
    
mqttBroker = '10.245.151.187'
topicSub = 'Three/tell'
topicPub = 'Three/listen'
clientID = 'Jacob_Suely_ESP'

def whenCalled(topic, msg):
    time.sleep(0.5)

import mqtt_CBR
mqtt_CBR.connect_wifi(Tufts_Wireless)
client = mqtt_CBR.mqtt_client(clientID, mqttBroker, whenCalled)
client.publish(topicPub, "1")
'''

ESP_code_reverse = '''
from secrets import *
from serial import *
import time
    
mqttBroker = '10.245.151.187'
topicSub = 'Three/tell'
topicPub = 'Three/listen'
clientID = 'Jacob_Suely_ESP'

def whenCalled(topic, msg):
    time.sleep(0.5)

import mqtt_CBR
mqtt_CBR.connect_wifi(Tufts_Wireless)
client = mqtt_CBR.mqtt_client(clientID, mqttBroker, whenCalled)
client.publish(topicPub, "4")
'''

# accelListen() waits for threshold accelorometer reading to be reached
def accelListen():
    keepLooping = True
    while (keepLooping):
        accel_data_arr = lsm.read_accel() # read accelerometer data into an array
        accel_data_x = accel_data_arr[0] # interested in changes in x position only
        print(accel_data_x)
        
        if (accel_data_x > accel_x_threshold_pos):
            keepLooping = False
            return 1
        elif (accel_data_x < accel_x_threshold_neg):
            keepLogging = False
            return 0
        time.sleep(1)

# startESP8266() actually serially communicates to the ESP8266
def startESP8266(s, code):
    print("Opening serial line to ESP8266...")

    s.send_code(code) # Sending code to ESP8266
    time.sleep(3) # buffer time -> to prevent overflowing ESP8266

# main()
def main():
    s = serial_comm(115200)
    s.abort()
    while True:
        direction = accelListen()
        if (direction == 1):
            startESP8266(s, ESP_code_forward)
        elif (direction == 0):
            startESP8266(s, ESP_code_reverse)
        time.sleep(1)

