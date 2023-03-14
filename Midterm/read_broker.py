'''

read_broker.py
ME35 Midterm
By: Jacob Choi

- Subscribes to the "angles" MQTT topic and continuously updates a drawing representing
the current position of the two links

'''

import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import math
import requests
from mySecrets import *

theta1 = []
theta2 = []

L1 = 7 # shoulder length (cm)
L2 = 13 # leg length (cm)

                ## Initializing plot to update ## 

plt.ion()
figure, ax = plt.subplots(figsize=(10, 8))
line1, = ax.plot([0, -5.562148865321747], [0, -4.25], label="Shoulder Link")
line2, = ax.plot([-5.562148865321747, 0], [-4.25, -16], label="Leg Link")
plt.title("Current Link Locations")
plt.legend(loc="upper right")
plt.xlabel("x-position (cm)")
plt.ylabel("y-position (cm)")
plt.xlim(-12, 15)
plt.ylim(-20, 5)

joint1_URL = 'https://io.adafruit.com/api/v2/jchoi2507/feeds/joint-1-angles/data'
joint2_URL = 'https://io.adafruit.com/api/v2/jchoi2507/feeds/joint-2-angles/data'

                ## Posting to Adafruit.io dashboard through REST API ##

def postAngles(angle1, angle2):
    data1 = {"datum": {"value": angle1}}
    data2 = {"datum": {"value": angle2}}
    requests.post(joint1_URL, headers=AIOKEY, json=data1)
    requests.post(joint2_URL, headers=AIOKEY, json=data2)

                ## Updates the plot to match current position of links ##

def updateGraph(angle1, angle2):
    # Reverting from motor angles -> regular angles
    angle1 = -1 * angle1
    angle2 = -1 * angle2

    # Initial position is the x & y location of shoulder link
        # Need to subtract by pi/2 to rotate axes by 1 quadrant
    x1 = L1 * math.cos(math.radians(angle1) - math.pi/2)
    y1 = L1 * math.sin(math.radians(angle1) - math.pi/2)

    # End position is the sum of x & y location of shoulder + leg links
        # Need to subtract by pi/2 to rotate axes by 1 quadrant
    x2 = x1 + (L2 * math.cos(math.radians(angle1) + math.radians(angle2) - math.pi/2))
    y2 = y1 + (L2 * math.sin(math.radians(angle1) + math.radians(angle2) - math.pi/2))

    # Updating plot every function call
    line1.set_xdata([0, x1])
    line1.set_ydata([0, y1])
    line2.set_xdata([x1, x2])
    line2.set_ydata([y1, y2])

    figure.canvas.draw()
    figure.canvas.flush_events()

                ## Retrieves MQTT message and calls updateGraph() ##

def on_message(client, userdata, message):
    message = str(message.payload.decode("utf-8"))
    if (message[0] == "("): # Checking to see if a pair of angles was provided
        angle1 = ""
        digit = ""
        for i in range(1, 4): # 4 is arbitrary and can be increased to improve accuracy but not necessary
            digit = message[i]
            angle1 = angle1 + digit
        
        angle2 = message[message.index(",") + 1:] # Indexing AFTER the comma, indicating leg motor angle
        angle2 = angle2[:-1] # Removing closing parantheses

    postAngles(angle1, angle2)
    updateGraph(float(angle1), float(angle2))

# MQTT loop
client = mqtt.Client("read_broker")
client.connect("10.0.0.125")
client.subscribe("angles")

client.on_message = on_message
client.loop_forever()
