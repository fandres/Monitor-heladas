import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

msg_temp = subscribe.simple("/cultivo/temp", hostname="169.254.176.163")
msg_hum = subscribe.simple("/cultivo/hum", hostname="169.254.176.163")

# Debug
print("%s %s" % (msg_temp.topic, msg_temp.payload))
print("%s %s" % (msg_hum.topic, msg_hum.payload))


if float(msg_temp.payload) <= 30 and float(msg_hum.payload) > 55:
    print(" Helada")
    publish.single("/cultivo/alarma", "on", hostname="169.254.176.163")
