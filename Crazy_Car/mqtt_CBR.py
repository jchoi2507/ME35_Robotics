from umqtt_simple import MQTTClient
import network, ubinascii
from socket import socket
import time

def connect_wifi(wifi):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print("MAC " + mac)
    
    station.connect(wifi['ssid'],wifi['pass'])
    while not station.isconnected():
        time.sleep(1)
    print('Connection successful')
    print(station.ifconfig())
    
def chuck_check():
    r=requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    print(data)

class mqtt_client():
    def __init__(self, my_id, serverURL, callback_function):
        self.URL = serverURL
        self.id = my_id
        self.client = None
        self.callback = callback_function
        self.try_to_connect()
        
    def try_to_connect(self):
        try:
            self.client = MQTTClient(self.id, self.URL, keepalive=60)
            print('Connected to %s MQTT broker' % (self.URL))
            self.client.connect()
            self.client.set_callback(self.callback)
            return True
        except OSError as e:
            print('Failed to connect to %s' % (self.URL))
            return False
            
    def connect(self):
        while not self.try_to_connect():
            print('restarting...')
            time.sleep(10)
            machine.reset()
            
    def check(self):
        self.client.check_msg()
            
    def disconnect(self):
        self.client.disconnect()

    def subscribe(self, topic_sub):
        print(topic_sub)
        self.client.subscribe(topic_sub.encode())
        
    def publish(self, topic_pub, msg):
        self.client.publish(topic_pub.encode(),msg.encode())
