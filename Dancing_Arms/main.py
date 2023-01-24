from motorController import *
from MC_Consts import *
import time
from lsm6dsox import LSM6DSOX

from machine import Pin, I2C
lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))

## Can loop through servo ports on the board ##

# servos = []
# for i in range(4):
#    servos.append(Servo(i))

## Setting up servo object ##
servo = Servo(1)

while True:
    accel_data_arr = lsm.read_accel() # read accelerometer data into an array
    accel_data_x = accel_data_arr[0] # interested in changes in x position only
    # print(accel_data_arr)
    # print(accel_data_x)

    angleChange = 225 * accel_data_x # multiply by 225 to propagate servo movement
    print(angleChange)
    
    ## A series of checks to determine if the servo should NOT output movement based on inputted accelorometer data
    if angleChange < 0:
        angleChange = 0.0 # Can't change servo to a negative angle value, so ignore accelorometer data in negative range
    if angleChange > 180.0:
        angleChange = 180.0 # Servo movements limited from 0-180 degrees, therefore any angleChange > 180 should just be set at the max 180 degrees

    servo.setAngle(int(angleChange))
    time.sleep(1) # buffer time
