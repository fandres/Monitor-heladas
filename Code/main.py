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
    Pin 4   ->  Pin sensor(DHT11/DHT22)
    Pin 2   ->  Debug Visual(Default=Off), Led On Userled: for development board ESP8266
    Pin 3   ->  Interrupt(Default=Off), Interrupt: rising and falling edge()
    Pin 0  ->  Break loop, [High = break]
"""
import time
import machine
import esp
import dht


class Monitoreo():
    "Clase padre, Monitoreo del dispositivo para micropython: "
    def __init__(self, pin_dht=4, sensor="DHT22", pin_break_=0):
        self.pin_DHT = pin_dht
        self.sensor_type = sensor
        self.pin_break_loop = pin_break_
        self.pin_break = machine.Pin(self.pin_break_loop, machine.Pin.IN, machine.Pin.PULL_UP)  # Break loop, Pin:[High = break]
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
        if self.pin_break.value() == 0:
            self.break_loop = 1
        else:
            self.break_loop = 0  # Termina el loop
            if self.debug_mode == 1:
                print("Termino el ciclo por hardware [High = break] Pin: ", self.pin_break_loop)
                self.pin_led_debug.value(0)  # Debug visual

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
            self.file.write(str(self.s_dht.temperature())+", "+str(self.s_dht.humidity())+"\n")
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
        pass

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
            sta_if.active(False)

    def configWifi(self):
        "Metodo usado para configurar lso parametros de la Red Wifi: SSID y PASSWORD"
        pass

    def wifiAP(self):
        "Crea un punto de acceso wifi, actua como anfitri?n"
        pass

    def wifiStation(self):
        "Hace de estaci?n (wifi) y se conecta con a un servidor u otro dispositivo"
        import network
        # Config
        WIFISSID = "Koen"
        WIFIPASS = "/*Casa*/"
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect(WIFISSID, WIFIPASS)
            while not sta_if.isconnected():
                print('network config:', sta_if.ifconfig())

    def MQTTclient(self):
        "Protocolo MQTT en modo cliente, usado apra enviar los datos"
        from time import sleep_ms
        from ubinascii import hexlify
        from machine import unique_id
        from umqtt import MQTTClient  # import socket
        # Config
        SERVER = "192.168.0.101"
        CLIENT_ID = hexlify(unique_id())
        TOPIC1 = b"/cultivo/tem"
        TOPIC2 = b"/cultivo/hum"
        TOPIC3 = b"/sensor1/led"
        try:
            client_mqtt = MQTTClient(CLIENT_ID, server)
            client_mqtt.connect()
            client_mqtt.publish(topic, dato)
            sleep_ms(200)
            client_mqtt.disconnect()
        except Exception as e:
            pass

    def interruptMode(self, mode=0):
        "Activa/Desactiva las interrupciones, por tiempo y por cambio de flanco, On:1 | Off:0"
        self.interrupt_mode = mode
        if self.interrupt_mode == 1:
            self.p_interrupt = machine.Pin(3, machine.Pin.IN)  # Interupt por cambio de flanco
            # Flanco de bajada y flanco de subida rising and falling edge()
            self.p_interrupt.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.callback)

    def callback(self, p):
        "Metodo que se ejecuta una vez ocurrida la interrupci?n"
        # print('pin change', p)
        self.break_loop = 0

    def loop(self):
        "Bucle principal en espera de flanco"
        while self.break_loop == 1:  # beak: interrupt, Pin change
            # Sleep Off
            self.readData()  # Lectura de sensores
            self.saveData()  # si esta ctiva almacena datos
            # Sleep On
            self.pinEndUp()
            time.sleep(1)
        self.saveData()


if __name__ == '__main__':
    ESP8266 = Monitoreo()
    try:
        ESP8266.wifi(1)
        ESP8266.debugMode(1)
        ESP8266.sensorConected("DHT22")
        ESP8266.sensorConected("DHT11")
        ESP8266.MQTTclient()
        ESP8266.loop()
    finally:
        pass