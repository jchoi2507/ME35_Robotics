from motorController import *
from MC_Consts import *
from machine import Pin, ADC
import time
import math

lightSensor = ADC(Pin(29)) # Light sensor data attached
                           # to GPIO pin 29 on nano motor carrier board

servo = Servo(1) # Creating a Servo object

darkLightSensorArray = [] # Array for light sensor readings during motor training
ambientLightSensorArray = [] # Array for light sensor readings during motor training
brightLightSensorArray = [] # Array for light sensor readings during motor training

servoPositionDict = {"LOWEST": 180, "MEDIUM": 135, "HIGHEST": 90} # Dictionary for possible servo positions
    
PRECISION = 5 # Represents the number of data points the program will account for during training
              # Increasing PRECISIONN increases overall accuracy during training

# trainDark() is meant to initialize and train the motor in dark light conditions
def trainDark():
    while True:
        if (len(darkLightSensorArray) == PRECISION): # If the array length is equal to the precision, training is finished
        
            sumTotalReadings = 0 # Represents the sum of all array elements
        
            for i in range(len(darkLightSensorArray)):
                sumTotalReadings = sumTotalReadings + darkLightSensorArray[i]
            
            average = sumTotalReadings/PRECISION # Computing average of the sum
            
            print("\n")
            print("Dark training completed! with an average of:", average)
            print("\n")
            return average
            break
        
        value = lightSensor.read_u16() 
        darkLightSensorArray.append(value) # Storing light sensor reading in array
        
        print("Current reading is:", value)
        time.sleep(1) # buffer time

# trainAmbient() is meant to initialize and train the motor in ambient light conditions
def trainAmbient():
    while True:
        if (len(ambientLightSensorArray) == PRECISION): # If the array length is equal to the precision, training is finished
        
            sumTotalReadings = 0 # Represents the sum of all array elements
        
            for i in range(len(ambientLightSensorArray)):
                sumTotalReadings = sumTotalReadings + ambientLightSensorArray[i]
            
            average = sumTotalReadings/PRECISION # Computing average of the sum
            
            print("\n")
            print("Ambient training completed! with an average of:", average)
            print("\n")
            return average
            break
        
        value = lightSensor.read_u16()
        ambientLightSensorArray.append(value) # Storing light sensor reading in array
        
        print("Current reading is:", value)
      
        time.sleep(1) # buffer time

# trainBright() is meant to initialize and train the motor in bright light conditions
def trainBright():
    while True:
        if (len(brightLightSensorArray) == PRECISION): # If the array length is equal to the precision, training is finished
        
            sumTotalReadings = 0
        
            for i in range(len(brightLightSensorArray)):
                sumTotalReadings = sumTotalReadings + brightLightSensorArray[i]
            
            average = sumTotalReadings/PRECISION # Computing average of the sum
            
            print("\n")
            print("Bright training completed! with an average of:", average)
            print("\n")
            
            return average
            break
        
        value = lightSensor.read_u16()
        brightLightSensorArray.append(value) # Storing light sensor reading in array
        
        print("Current reading is:", value)
      
        time.sleep(1) # buffer time

# Meant to be used post-training, diffCalculator() determines whether a light sensor reading is closest to dark, ambient, or bright light conditions
def diffCalculator(darkAverage, ambientAverage, brightAverage):
    value = lightSensor.read_u16() # Read light sensor reading
    avgArray = [darkAverage, ambientAverage, brightAverage] # Array representing the 3 averages from training
    diffArray = [abs(value - darkAverage), abs(value - ambientAverage), abs(value - brightAverage)] # Array representing the absolute value difference
    
    closestTo = diffArray.index(min(diffArray)) # Finding the index where the difference is the smallest
    
    if (closestTo == 0):
        return "LOWEST"
    elif (closestTo == 1):
        return "MEDIUM"
    elif (closestTo == 2):
        return "HIGHEST"

# makeMyServoSmart() is the function that moves the servo based on training
def makeMyServoSmart(darkAverage, ambientAverage, brightAverage):
    while True:   
        anglePosition = diffCalculator(darkAverage, ambientAverage, brightAverage)
        servo.setAngle(servoPositionDict[anglePosition])
        time.sleep(1) # buffer time

while True:
    print("**** SMART MOTOR TRAINING ****\n")
    time.sleep(1)
    
    ## DARK TRAINING ##
    print("Dark training beginning in:\n")
    print("3...\n")
    time.sleep(1)
    print("2...\n")
    time.sleep(1)
    print("1...\n")
    time.sleep(1)
    darkAverage = trainDark()
    time.sleep(1)
    
    ## AMBIENT TRAINING ##
    print("Ambient training beginning in:\n")
    print("3...\n")
    time.sleep(1)
    print("2...\n")
    time.sleep(1)
    print("1...\n")
    time.sleep(1)
    ambientAverage = trainAmbient()
    time.sleep(1)
    
    ## BRIGHT TRAINING ##
    print("Bright training about to begin! Prepare a flashlight\n") # A little heads up :)
    time.sleep(3)
    print("Bright training beginning in:\n")
    print("3...\n")
    time.sleep(1)
    print("2...\n")
    time.sleep(1)
    print("1...\n")
    time.sleep(1)
    brightAverage = trainBright()
    time.sleep(1)

    print("Training completed. Interact with the animal!\n")
    
    makeMyServoSmart(darkAverage, ambientAverage, brightAverage)
