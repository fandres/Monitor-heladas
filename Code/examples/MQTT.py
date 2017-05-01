s_dht = dht.DHT22(machine.Pin(4))
s_dht.measure()
print("Temperatura ", s_dht.temperature())  # Debug

from time import sleep_ms
from ubinascii import hexlify
from machine import unique_id
from umqtt import MQTTClient  # import socket
# Config
SERVER = "192.168.31.16"
CLIENT_ID = hexlify(unique_id())
TOPIC1 = b"/cultivo/temp"
TOPIC2 = b"/cultivo/hum"
TOPIC3 = b"/sensor1/set/temp"
TOPIC4 = b"/sensor1/set/hum"
client_mqtt = MQTTClient(CLIENT_ID, SERVER)

client_mqtt.connect()
client_mqtt.publish(TOPIC1, str(s_dht.temperature()))
sleep_ms(200)
client_mqtt.disconnect()