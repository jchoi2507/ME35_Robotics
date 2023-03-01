mqtt_CBR.py: MQTT wifi connection + initialization, must be loaded onto both RP2040 & ESP8266

umqtt_simple.py: Dependency of mqtt_CBR.py, copied from (official branch)[https://github.com/jchoi2507/micropython-lib/blob/master/micropython/umqtt.simple/umqtt/simple.py]
                 due to firmware errors with using the native umqtt library. *On normal systems with umqtt importing correctly, rename all import instances
                 from "import umqtt_simple" to "import umqtt.simple"

serial.py: UART serial communication class, default constructor set to UART(0), which, on the ESP8266, means a baudrate of 115200
