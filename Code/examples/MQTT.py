from time import sleep_ms
from ubinascii import hexlify
from machine import unique_id
import machine
from umqtt import MQTTClient  # import socket
import dht

state = 0

led = machine.Pin(2, machine.Pin.OUT, value=1)
s_dht = dht.DHT22(machine.Pin(4))
s_dht.measure()
print("Temperatura ", s_dht.temperature())  # Debug
print("Temperatura ", s_dht.humidity())  # Debug

# Config
SERVER = "192.168.31.16"
CLIENT_ID = hexlify(unique_id())
TOPIC1 = b"/cultivo/temp"
TOPIC2 = b"/cultivo/hum"
TOPIC3 = b"/sensor1/set/temp"
TOPIC4 = b"/sensor1/set/hum"
TOPIC5 = b"/cultivo/alarma"
state = 0
client_mqtt = MQTTClient(CLIENT_ID, SERVER)
# Envio
client_mqtt.connect()
client_mqtt.publish(TOPIC1, str(s_dht.temperature()))
client_mqtt.publish(TOPIC2, str(s_dht.humidity()))
sleep_ms(200)
client_mqtt.disconnect()


# Recepcion
def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == b"on":
        led.value(0)
        state = 1
    elif msg == b"off":
        led.value(1)
        state = 0
    elif msg == b"toggle":
        # LED is inversed, so setting it to current state
        # value will make it toggle
        led.value(state)


state = 1 - state
client_mqtt = MQTTClient(CLIENT_ID, SERVER)
# Subscribed messages will be delivered to this callback
client_mqtt.set_callback(sub_cb)
client_mqtt.connect()
client_mqtt.subscribe(TOPIC5)
print("Connected to %s, subscribed to %s topic" % (SERVER, TOPIC5))

try:
    while 1:
        # micropython.mem_info()
        client_mqtt.wait_msg()
finally:
    client_mqtt.disconnect()
