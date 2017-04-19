"""
    This software is free, licensed under GPL v3.
    Author - Fabian A. Salamanca F.

    Pin distribution(Default)
    Pin 4   ->  Pin sensor(DHT11/DHT22)
    Pin 2   ->  Debug Visual(Default=Off), Led On Userled: for development board ESP8266
    Pin 3   ->  Interrupt(Default=Off), Interrupt: rising and falling edge()

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
        self.dataWrite = 0  # Almacena los datos, On:1 | Off:0
        self.file = open('data.txt', 'w')
        self.break_loop = 1  # Termina el loop mediante interropciones o Cambie de estado de pin
        self.interrupt_mode = 0  # Activa/Desactiva las interrupciones por tiempo/pin: On:1 | Off:0
        self.debug_mode = 0  # Debuf On:1 | Off:0
        self.sensorConected()

    def sensorConected(self):
        "Conmuta entre lso diferentes sensores: DHT11/DHT22"
        if self.sensor_type == "DHT22":
            self.s_dht = dht.DHT22(machine.Pin(self.pin_DHT))
        elif self.sensor_type == "DHT11":
            self.s_dht = dht.DHT11(machine.Pin(self.pin_DHT))
        else:
            if self.debug_mode == 1:
                print("Sensor inadecuado, elija entre las opciones: DHT11 o DHT22")  # debug
                self.pin_led_debug.value(not self.pin_led_debug.value())  # Debug visual

    def debugMode(self, mode=0):
        "Activa/Desactiva El debug visual y de consola"
        self.debug_mode = mode
        if self.debug_mode == 1:
            esp.osdebug(1)  # turn on/off vendor O/S debugging messages
            self.pin_led_debug = machine.Pin(2, machine.Pin.OUT)  # Debug visual
        else:
            esp.osdebug(0)

    def saveData(self):
        "Guarda los datos en un archivo"
        if self.dataWrite == 1:
            self.dataWrite = 2
            self.file.write("TEMP, HUM\n")
        elif self.dataWrite == 2:
            self.file.write(str(self.s_dht.temperature())+", "+str(self.s_dht.humidity())+"\n")
        elif self.dataWrite == 0:
            self.dataWrite = 3
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

    def wifi(self):
        "Activa/Desactiva el Wifi "
        pass

    def wifiAP(self):
        "Crea un punto de acceso wifi, actua como anfitrión"
        pass

    def wifiStation(self):
        "Hace de estación y se conecta con a un servidor u otro dispositivo"
        pass

    def interruptMode(self, mode=0):
        "Activa/Desactiva las interrupciones, por tiempo y por cambio de flanco"
        self.interrupt_mode = mode
        if self.interrupt_mode == 1:
            self.p_interrupt = machine.Pin(3, machine.Pin.IN)  # Interupt por cambio de flanco
            # Flanco de bajada y flanco de subida rising and falling edge()
            self.p_interrupt.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.callback)

    def callback(self, p):
        "Metodo que se ejecuta una vez ocurrida la interrupción"
        # print('pin change', p)
        self.break_loop = 0

    def loop(self):
        "Bucle principal en espera de flanco"
        while self.break_loop == 1:  # beak: interrupt, Pin change
            # Sleep Off
            self.readData()  # Lectura de sensores
            self.saveData()  # si esta ctiva almacena datos
            # Sleep On
            time.sleep(1)
        self.saveData()


ESP8266 = Monitoreo()
ESP8266.debugMode(1)
ESP8266.loop()
