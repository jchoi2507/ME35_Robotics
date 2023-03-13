'''

spline_trajectory.py
ME35 Midterm
By: Jacob Choi

- Given an [x, y] range of data sets, interpolates a cubic spline based trajectory
    - Validates trajectory
- Performs inverse kinematics calculations to determine necessary theta1 (joint 1 angle)
and theta2 (joint 2 angle) rotations of respective motors
    - Validates angle values
- Outputs angular values into a JSON file for RP2040 use

'''

from scipy.interpolate import CubicSpline
import serial
import matplotlib.pyplot as plt
import math
import numpy as np
import json
import time
import requests
from mySecrets import *

L1 = 7 # shoulder length (cm)
L2 = 13 # leg length (cm)

s = serial.Serial('/dev/cu.usbmodem14101', 115200)
URL = 'https://io.adafruit.com/api/v2/jchoi2507/feeds/start-walking'

        ## Trajectory Calculation ##

def trajectory():
    x_start = 0 # Initial X start position (cm)
    x_stop = 12 # Desired X final position (cm)

    y_knots_original = [0, 1, 2, 3, 4, 5, 5, 5, 4, 3, 2, 1, 0] # Steps of Y position (cm)

    y_knots = []

    for i in range(len(y_knots_original) - 1):
        y_knots.append(y_knots_original[i] - 16)
    y_knots.append(-15.9)

    x_knots = np.linspace(x_start, x_stop, len(y_knots)) # Fitting spline through the "knot" points

    x_eval = np.linspace(x_start, x_stop, 200) # Plotting spline using the "evaluation" points

    traj = CubicSpline(x_knots, y_knots, bc_type='clamped') # Solving for spline trajectory

    # Plotting
    plt.plot(x_knots, y_knots, 'o')
    plt.plot(x_eval, traj(x_eval, 0))
    plt.xlim(x_start, x_stop)
    plt.ylim(-20, 5)
    plt.title("(x, y) Spline Trajectory (cm)")
    plt.xlabel('x-position (cm)')
    plt.ylabel('y-position (cm)')

    plt.show()

    return traj

            ## Inverse Kinematics Calculations ##

def inverseKinematics(traj):
    x_eval2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] # Updating x_eval to take in less points to prevent throttling
    coords = x_eval2, traj(x_eval2, 0)
    x_coords = coords[0] # x coordinates of points
    y_coords = coords[1].tolist() # y coordinates of points

    theta1_coord = []
    theta2_coord = []
    theta1_motor = []
    theta2_motor = []

    for i in range(len(x_coords)):
        x = -1 * y_coords[i] # adjusting for coordinate switch
        y = x_coords[i] # adjusting for coordinate switch

        L3 = math.sqrt(x**2 + y**2)

        alpha1 = math.acos((L2**2-L1**2-L3**2)/(-2*L1*L3))
        alpha2 = math.acos((L3**2-L1**2-L2**2)/(-2*L1*L2))

        # shoulderAngle_coord & legAngle_coord are the COORDINATE-PLANE angle values
        shoulderAngle_coord = (math.degrees(math.atan(y/x)) - math.degrees(alpha1))
        legAngle_coord = (180 - math.degrees(alpha2))

        theta1_coord.append(shoulderAngle_coord)
        theta2_coord.append(legAngle_coord)

        # shoulderAngle_motor & legAngle_motor are the ACTUAL angle values to send to the motor
            # Need to multiply by -1 to account that motor CW = +
        shoulderAngle_motor = -1 * shoulderAngle_coord
        legAngle_motor = -1 * legAngle_coord

        theta1_motor.append(shoulderAngle_motor)
        theta2_motor.append(legAngle_motor)

    # Outputting MOTOR angles into a JSON file
    file = open("motor_angles.txt", "w")
    json.dump([theta1_motor, theta2_motor], file)
    file.close()

    # Returning COORD angles for validation simulation below...NOT the modified motor angles
    return theta1_coord, theta2_coord

                ## Validating angle values through forward kinematics ##

def animatedIKPlot(theta1, theta2):
    fileNameCounter = 1
    counter = 0

    for i in theta1:
        # x & y locations of shoulder link
            # Need to subtract by pi/2 to rotate axes by 1 quadrant
        x1 = L1 * math.cos(math.radians(i) - math.pi/2)
        y1 = L1 * math.sin(math.radians(i) - math.pi/2)

        # x & locations of leg link is the sum of x & y location of shoulder + leg links
            # Need to subtract by pi/2 to rotate axes by 1 quadrant
        x2 = x1 + (L2 * math.cos(math.radians(i) + math.radians(theta2[counter]) - math.pi/2))
        y2 = y1 + (L2 * math.sin(math.radians(i) + math.radians(theta2[counter]) - math.pi/2))

        filename = str(fileNameCounter) + ".png"
        fileNameCounter += 1

        # Plotting an animation
        plt.figure(counter)
        plt.plot([0, x1], [0, y1], 'r', label="Shoulder Link")
        plt.plot([x1, x2], [y1, y2], 'b', label="Leg Link")
        plt.title("Motor Angle Validation Plot")
        plt.legend(loc="upper right")
        plt.xlabel("x-position (cm)")
        plt.ylabel("y-position (cm)")
        plt.xlim(-12, 15)
        plt.ylim(-20, 5)
        plt.savefig(filename)

        counter += 1

                ## Waits for Adafruit start button to turn on, then starts RP2040 script ##

def startRP2040():
    keepLooping = True
    while (keepLooping):
        r = requests.get(URL, headers=AIOKEY)
        data = r.json()
        field = data['last_value']

        if (field == "1"): # Adafruit field of int: 1 -> start walking!
            keepLooping = False

        else:
            #print("Waiting for command to execute...")
            continue

        time.sleep(0.5)
    print("Starting to walk!...")
    s.write(b'import motor_control\r\n')
    s.write(b'motor_control.main()\r\n') # Run main() in motor_control.py on RP2040

if __name__ == "__main__":
    traj = trajectory()
    theta1, theta2 = inverseKinematics(traj)
    animatedIKPlot(theta1, theta2)
    startRP2040()
