import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
from time import sleep


HOSTNAME = "169.254.176.163"
PIN_ALARMA = 17
PIN_STOP_ALARMA = 4
SET_TEMP = 30
SET_HUM = 55
alarm_state = 0


def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_ALARMA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_STOP_ALARMA, GPIO.IN, pull_up_down = GPIO.PUD_UP)  # Entrada

msg_temp = subscribe.simple("/cultivo/temp", hostname=HOSTNAME)
msg_hum = subscribe.simple("/cultivo/hum", hostname=HOSTNAME)

# Debug
print("%s %s" % (msg_temp.topic, msg_temp.payload))
print("%s %s" % (msg_hum.topic, msg_hum.payload))


while True:
    if float(msg_temp.payload) <= SET_TEMP and float(msg_hum.payload) > SET_HUM:
        print(" Helada! Ring Ring")
        if GPIO.input(PIN_STOP_ALARMA) == 1:
            alarm_state = 1
            publish.single("/cultivo/alarma", "Alarma Apagada", hostname=HOSTNAME)
        sleep(0.5)
        if alarm_state == 0:
            publish.single("/cultivo/alarma", "on", hostname=HOSTNAME)
            GPIO.output(PIN_ALARMA, True)
        else:
            GPIO.output(PIN_ALARMA, False)
            publish.single("/cultivo/alarma", "off", hostname=HOSTNAME)
        #sleep(1)
else:
    GPIO.cleanup()
