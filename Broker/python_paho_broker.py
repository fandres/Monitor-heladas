import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))

mqttc = mqtt.Client()
mqttc.on_connect = on_connect

msg_temp = subscribe.simple("/cultivo/temp", hostname="169.254.176.163")
msg_hum = subscribe.simple("/cultivo/hum", hostname="169.254.176.163")

# Debug
print("%s %s" % (msg_temp.topic, msg_temp.payload))
print("%s %s" % (msg_hum.topic, msg_hum.payload))

if float(msg_temp.payload) == 0:
    print(" Hielo")
