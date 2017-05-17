"""
    DESCRIPCI?N...
    This software is free, licensed y distributed under GPL v3.
    (see COPYING) WITHOUT ANY WARRANTY.
    You can see a description of license here: http://www.gnu.org/copyleft/gpl.html
    Copyright(c) 2017 by fandres "Fabian Salamanca" <fabian.salamanca@openmailbox.org>
                      by CH3 "Christian Camilo Cardenas <christian.camilo.cardenas@gmail.com>"
    Distributed under GPLv3+
    Hardware: ESP8266
    Pin distribution(Default)
    Pin 17 [GPIO.BCM]   ->  Pin: Alarm(Buzer): [OUT]
    Pin 4 [GPIO.BCM]    ->  Pin: Stop Alarm(Buzer): [OUT]
    Configure wifi and MQTT
    library:
    https://github.com/eclipse/paho.mqtt.python
"""

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
from time import sleep


HOSTNAME = "169.254.176.163"  # <---------------------- CONFIGURE BROKER ADDRESS
PIN_ALARMA = 17
PIN_STOP_ALARMA = 4
SET_TEMP = 30
SET_HUM = 55
TIME_SLEEP_ALARMA = 10
alarm_state = 0
count_alarma = 0


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


try:
    while True:
        #print("%s %s" % (msg_temp.topic, msg_temp.payload))
        #print("%s %s" % (msg_hum.topic, msg_hum.payload))
        "Estado de Alarma"
        if float(msg_temp.payload) <= SET_TEMP and float(msg_hum.payload) > SET_HUM:
            print(" Helada! Ring Ring")
            if GPIO.input(PIN_STOP_ALARMA) == 1:
                alarm_state = 1
                publish.single("/cultivo/alarma", "Alarma Apagada", hostname=HOSTNAME)
                count_alarma = 1
                sleep(0.2)
            if alarm_state == 0:
                publish.single("/cultivo/alarma", "on", hostname=HOSTNAME)
                GPIO.output(PIN_ALARMA, True)
            else:
                GPIO.output(PIN_ALARMA, False)
                publish.single("/cultivo/alarma", "off", hostname=HOSTNAME)
                if count_alarma >= 1 and count_alarma < TIME_SLEEP_ALARMA:
                    count_alarma += 1
                    sleep(0.5)
                elif count_alarma == TIME_SLEEP_ALARMA:
                    count_alarma = 0
                    alarm_state = 0
        elif count_alarma == TIME_SLEEP_ALARMA:
            count_alarma = 0
finally:
    GPIO.cleanup()
