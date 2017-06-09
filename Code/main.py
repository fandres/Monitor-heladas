"""
    DESCRIPCI?N...
    This software is free, licensed y distributed under GPL v3.
    (see COPYING) WITHOUT ANY WARRANTY.
    You can see a description of license here: http://www.gnu.org/copyleft/gpl.html
    Copyright(c) 2017 by fandres "Fabian Salamanca" <fabian.salamanca@openmailbox.org>
    Distributed under GPLv3+
    Author - Fabian A. Salamanca F.

    Hardware: ESP8266
    Pin distribution(Default)
    Pin 4   ->  Pin sensor(DHT11/DHT22), Data(IN)
    Pin 16  ->  Pin Alarm (OUT)
    Pin 5   ->  Pin, Stop alarm (IN)
    Pin 2   ->  Debug Visual(Default=Off), Led On Userled: for development board ESP8266
    Pin 3   ->  Interrupt(Default=Off), Interrupt: rising and falling edge()
    Configure wifi and MQTT
"""
import time
import machine
import esp
import dht


class Monitoreo():
    "Clase padre, Monitoreo del dispositivo para micropython: "
    def __init__(self, pin_dht=4, sensor="DHT22"):
        self.pin_DHT = pin_dht
        self.sensor_type = sensor
        self.alarm_state = 0
        self.pin_alarma = machine.Pin(16, machine.Pin.OUT)  # Configure Pin: Alarma (OUT)
        self.pin_stopAlarm = machine.Pin(5, machine.Pin.OUT)  # Configure Pin: Stop Alarm (IN)
        self.count_alarma = 0
        self.alarma = 0
        self.time_active = 0
        self.dataWrite = 0  # Almacena los datos, On:1 | Off:0
        self.break_loop = 1  # variable para romper el loop
        self.interrupt_mode = 0  # interrupciones: On:1 | Off:0
        self.debug_mode = 0  # Debug On:1 | Off:0
        self.sensorConected()

    def sensorConected(self, sensor="DHT22"):
        "Conmuta entre los diferentes sensores: DHT11/DHT22"
        if self.sensor_type == "DHT22":
            self.s_dht = dht.DHT22(machine.Pin(self.pin_DHT))
        elif self.sensor_type == "DHT11":
            self.s_dht = dht.DHT11(machine.Pin(self.pin_DHT))
        else:
            if self.debug_mode == 1:
                print("Sensor inadecuado, elija entre las opciones: DHT11 o DHT22")  # debug
                self.pin_led_debug.value(not self.pin_led_debug.value())  # Debug visual

    def pinEndUp(self):
        "Rompe el loop por hardware, Pin:[High = break]"
        pass

    def debugMode(self, mode=0):
        "Activa/Desactiva El debug visual y de consola, On:1 | Off:0"
        self.debug_mode = mode
        if self.debug_mode == 1:
            esp.osdebug(1)  # turn on/off vendor O/S debugging messages
            self.pin_led_debug = machine.Pin(2, machine.Pin.OUT)  # Debug visual
        else:
            esp.osdebug(0)

    def saveData(self, mode=0):
        "Guarda los datos en un archivo, On:1 | Off:0"
        self.dataWrite = mode
        if self.dataWrite == 1:
            self.dataWrite = 2
            self.file = open('data.txt', 'w')
            self.file.write("TEMP, HUM\n")
        elif self.dataWrite == 2:
            self.file.write(str(self.s_dht.temperature())+", \
                          "+str(self.s_dht.humidity())+"\n")
        elif self.dataWrite == 0:
            self.dataWrite = 3
            self.file = open('data.txt', 'w')
            self.file.write("Data storage off\n")
            self.file.close()

    def readData(self):
        "Obtiene de lso sensores los datos de Temperatura/Humedad"
        self.s_dht.measure()
        if self.debug_mode == 1:
            print("Temperatura ", self.s_dht.temperature())  # Debug
            print("Humedad  ", self.s_dht.humidity())  # Debug
            self.pin_led_debug.value(not self.pin_led_debug.value())  # Debug visual

    def actuators(self):
        "Activa la logica de los Actuadores"
        # if self.pin_stopAlarm.value() == 1:  # MQTT Or Pin
        #     self.alarma = 0
        if self.s_dht.temperature() == 3 and self.s_dht.humidity() >= 85:
            self.alarma = 1
            self.time_active = 60
        elif self.s_dht.temperature() == 1 and self.s_dht.humidity() >= 92:
            self.pin_alarma = 1
            self.time_active = 300
        if self.alarma == 1 and self.count_alarma <= self.time_active:
            self.pin_alarma.high()
            self.count_alarma += 1
            if self.count_alarma == self.time_active:
                self.pin_alarma.low()
                self.count_alarma = 0
            if self.debug_mode == 1:
                print("Estado del actuador en: "+self.value(16)+" Pin No.", self.pin_alarma)
                self.pin_led_debug.value(not self.pin_led_debug.value())  # Debug visual
        else:
            self.count_alarma = 0

    def sleepMode(self):
        " Duerme el dispositivo"
        pass

    def wifi(self, mode=1):
        "Activa/Desactiva el Wifi "
        self.wifi_switch = mode
        if self.wifi_switch == 1:
            self.configWifi()
            self.wifiStation()
        elif self.wifi_switch == 1:
            self.sta_if.active(False)

    def configWifi(self):
        "Metodo usado para configurar los parametros de la Red Wifi: SSID y PASSWORD"
        pass

    def wifiAP(self):
        "Crea un punto de acceso wifi, actua como anfitri?n"
        pass

    def wifiStation(self):
        "Hace de estaci?n (wifi) y se conecta con a un servidor u otro dispositivo"
        import network
        # Config
        WIFISSID = "Cultivo_pi"  # <-----------------CONFIGURE: SDID de Red wifi
        WIFIPASS = "raspberry"  # <-----------------CONFIGURE: PASSWORD de Red wifi
        self.sta_if = network.WLAN(network.STA_IF)
        if not self.sta_if.isconnected():
            print('connecting to network...')
            self.sta_if.active(True)
            self.sta_if.connect(WIFISSID, WIFIPASS)
            while not self.sta_if.isconnected():
                print('network config:', self.sta_if.ifconfig())

    def MQTTclient(self):
        "Protocolo MQTT en modo cliente, Configuración"
        from ubinascii import hexlify
        from machine import unique_id
        from umqtt import MQTTClient  # import socket library (umqtt)
        # Config
        SERVER = "172.24.1.1"  # <----------------------------CONFIGURE: BROKER
        CLIENT_ID = hexlify(unique_id())
        self.TOPIC1 = b"/cultivo/temp"
        self.TOPIC2 = b"/cultivo/hum"
        self.TOPIC3 = b"/sensor1/set/temp"
        self.TOPIC4 = b"/sensor1/set/hum"
        self.TOPIC5 = b"/sensor1/alarma"
        self.client_mqtt = MQTTClient(CLIENT_ID, SERVER)

    def MQTTSend(self):
        "Envio Datos mediante el protocolo MQTT"
        try:
            self.client_mqtt.connect()
            self.client_mqtt.publish(self.TOPIC1, str(self.s_dht.temperature()))
            self.client_mqtt.publish(self.TOPIC2, str(self.s_dht.humidity()))
            time.sleep_ms(200)
            self.client_mqtt.disconnect()
        except Exception as e:
            pass

    def MQTTReceive(self):
        "Metodo que recibe datos enviados a traves del protocolo MQTT"
        self.alarm_state = 1 - self.alarm_state
        # Subscribed messages will be delivered to this callback
        self.client_mqtt.set_callback(self.sub_cb)
        self.client_mqtt.connect()
        self.client_mqtt.subscribe(self.TOPIC5)

    def sub_cb(self, topic, msg):
        "Recepcion MQTT"
        print((topic, msg))
        if msg == b"on":
            self.pin_led_debug.value(0)
            self.alarm_state = 1
        elif msg == b"off":
            self.pin_led_debug.value(1)
            self.alarm_state = 0
        elif msg == b"toggle":
            self.pin_led_debug.value(self.alarm_state)

    def interruptMode(self, mode=0):
        "Activa/Desactiva las interrupciones, por tiempo y por cambio de flanco, On:1 | Off:0"
        self.interrupt_mode = mode
        if self.interrupt_mode == 1:
            self.p_interrupt = machine.Pin(3, machine.Pin.IN)  # Interupt por cambio de flanco
            # Flanco de bajada y flanco de subida rising and falling edge()
            self.p_interrupt.irq(trigger=machine.Pin.IRQ_RISING |
                                 machine.Pin.IRQ_FALLING, handler=self.callback)

    def callback(self, p):
        "Metodo que se ejecuta una vez ocurrida la interrupci?n"
        # print('pin change', p)
        self.break_loop = 0

    def loop(self):
        "Bucle principal infinito"
        while True:  # beak: interrupt, Pin change
            # Sleep Off
            self.readData()  # Lectura de sensores
            # self.saveData()  # si esta activa, almacena datos
            self.MQTTSend()  # Enviar datos mediante el protocolo MQTT
            # self.client_mqtt.wait_msg()  # Recibe datos mediante el Protocolo MQTT
            # self.actuators()
            # Sleep On
            time.sleep(1)
            # self.pinEndUp()
            # micropython.mem_info()
        self.saveData()

#######################     MAIN    #######################
if __name__ == '__main__':
    ESP8266 = Monitoreo()
    try:
        ESP8266.wifi(1)
        ESP8266.debugMode(1)
        ESP8266.sensorConected("DHT22")
        # ESP8266.sensorConected("DHT11")
        ESP8266.MQTTclient()
        # ESP8266.MQTTReceive()
        ESP8266.loop()
    finally:
        pass
