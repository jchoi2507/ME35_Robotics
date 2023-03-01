# Block Diagram Overview
<p align="center">
  <img src="https://github.com/jchoi2507/ME35_Jacob/blob/main/Crazy_Car/IMG_0128.jpg" width="350" height="400">
</p>

# Include Files Explanation

- ME35HW6.py: Starting Python script

- RP2040_CrazyCar.py: MicroPython script that runs on RP2040

- EPS8266_CrazyCar.py: [optional] MicroPython script to run on ESP8266 at boot

- mqtt_CBR.py: MQTT wifi connection + initialization, must be loaded onto both RP2040 & ESP8266

- umqtt_simple.py: Dependency of mqtt_CBR.py, copied from [official branch](https://github.com/jchoi2507/micropython-lib/blob/master/micropython/umqtt.simple/umqtt/simple.py) due to firmware errors with using the native umqtt library. *On normal systems with umqtt importing correctly, rename all import instances from <code>import umqtt_simple</code> to <code>import umqtt.simple</code>

- serial.py: UART serial communication class, default constructor set to UART(0), which, on the ESP8266, means a baudrate of 115200, must be loaded onto both RP2040 & ESP8266

- secrets.py: WiFi login info, API base ID & token key & authentication headers

# Changes for Game Day

**All changes must be updated on both RP2040 & ESP8266**

- ME35HW6.py
    - Airtable API configurations (URL + headers)

- RP2040_CrazyCar.py
    - MQTT broker IP address
    - MQTT topic names
    - MQTT WiFi connection SSID 
    - MQTT published message/command

- secrets.py
    - Tufts_Secure SSID & pass info
