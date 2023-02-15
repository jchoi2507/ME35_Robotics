import time
import math
from motorController import *
from MC_Consts import *
from machine import Pin, ADC
from shape_functions import *

## Photo Art w/ 2 DOF Wooden Robotic Arm
## w/ Inverse Kinematics Implementetation

# Using the feedback from a DC motor encoder, 
# this code moves 2 DC motors on a 2 DOF robotic arm
# to a desired (x, y) position using
# inverse kinematics calculations

# An LED is also attached to the "end effector"

        ## INITIALIZATION ##

board = NanoMotorBoard()

ENCODER_360_ROTATION = 1100 # Encoder value at 360 degrees, @ duty cycle = 20
MULTIPLIER = 3.055 # Encoder transition pulse PER degree of rotation

# Robotic Arm Dimensions
L1 = 100 # mm
L2 = 100 # mm

# LED Setup
LED = Pin(29, Pin.OUT)
LED.value(1)

# Initialization function
def initialization():
    
    print("Rebooting...")
    board.reboot()
    time.sleep_ms(500)
    
    baseMotor = DCMotor(1) # Connected to first set of pins on RP2040
    armMotor = DCMotor(0) # Connected to second set of pins on RP2040

    baseMotor.setDuty(0)
    baseMotor.resetEncoder(0)
    armMotor.setDuty(0)
    armMotor.resetEncoder(0)
    
    return baseMotor, armMotor

    ## MOTOR MOVEMENT FUNCTIONS ##

# Resets motor positions to "origin" angles
def reset(baseMotor, armMotor):
    rotateByAngle(baseMotor, 0)
    rotateByAngle(armMotor, 0)

# Forward (CCW) motor movement function
def forward(motor):
    motor.setDuty(20)
    
# Reverse (CW) motor movement function
def reverse(motor):
    motor.setDuty(-20)
    
# Stop motor movement function
def stop(motor):  
    motor.setDuty(0)

# Move motor -> desired angle function
def rotateByAngle(motor, angle):
    encoderTarget = angle * MULTIPLIER
    
    if (angle == 0): # Resetting to initial position
        currEncoderValue = motor.readEncoder()
        if (currEncoderValue > 0):
            reverse(motor)
            while True:
                encoderValue = motor.readEncoder()
                if (encoderValue < 0):
                    stop(motor)
                    break
        elif (currEncoderValue < 0):
            forward(motor)
            while True:
                encoderValue = motor.readEncoder()
                if (encoderValue > 0):
                    stop(motor)
                    break

    elif (angle > 0): # CCW rotation
        forward(motor)
        while True:
            encoderValue = motor.readEncoder()
            if (encoderValue >= encoderTarget):
                stop(motor)
                #motor.resetEncoder(0)
                break
              
    elif (angle < 0): # CW rotation
        reverse(motor)
        while True:
            encoderValue = motor.readEncoder()
            if (encoderValue <= encoderTarget):
                stop(motor)
                #motor.resetEncoder(0)
                break

        ## INVERSE KINEMATICS FUNCTIONS ##

def inverseKinematics(baseMotor, armMotor, x, y):
    #x = int(input("Desired x position?\n"))
    #y = int(input("Desired y position?\n")
    
    L3 = math.sqrt(x**2 + y**2)
    alpha1 = math.acos((L2**2 - L1**2 - L3**2)/(-2*L1*L3))
    
    baseMotorAngle = math.degrees(math.atan2(y, x) - alpha1)
    print("Base Motor Angle: ", baseMotorAngle)
    
    rotateByAngle(baseMotor, baseMotorAngle)
    
    armMotorAngle = math.degrees(math.pi - math.acos((L3**2 - L1**2 - L2**2)/(-2*L1*L2)))
    print("Arm Motor Angle: ", armMotorAngle)
    
    rotateByAngle(armMotor, armMotorAngle)

baseMotor, armMotor = initialization()

#drawQuarterCircle_1(baseMotor, armMotor)
#drawCircle(baseMotor, armMotor)
#drawLine(baseMotor, armMotor)
#windshieldWiper_demo(baseMotor, armMotor)
