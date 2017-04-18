import time
import machine
import esp;
import dht


class Monitoreo():
    "Clase padre, Monitoreo del dispositivo para micropython: "
    def __init__(self):
        self.f = open('data.txt', 'w')
        self.dataWrite = 0  # Almacena los datos, On:1 | Off:0
        # self.s_dht = dht.DHT11(machine.Pin(4))
        self.s_dht = dht.DHT22(machine.Pin(4))
        self.sel = 1  # si hay interrupt
        self.p2 = machine.Pin(3, machine.Pin.IN)  # Interupt por cambio de flanco
        self.debug_mode = 1  # Debuf On:1 | Off:0
        self.startDev()

    def startDev(self):
        "Metodo que se ejecuta una vez inicializado el dispositivo y la clase"
        self.f.write("TEMEPRATURA, HUMEDAD\n")
        self.debugMode()

    def debugMode(self):
        "Activa/Desactiva El debug visual y de consola"
        if self.debug_mode == 1:
            esp.osdebug(1)  # turn on/off vendor O/S debugging messages
            self.pin_led = machine.Pin(2, machine.Pin.OUT)  # Debug visual
        else:
            esp.osdebug(0)

    def saveData(self):
        "Guarda los datos en un archivo"
        if self.dataWrite == 1:
            self.f.write(str(self.s_dht.temperature())+", "+str(self.s_dht.humidity())+"\n")
        else:
            self.f.close()

    def readData(self):
        "Obtiene de lso sensores los datos de Temperatura/Humedad"
        self.s_dht.measure()
        if self.debug_mode == 1:
            print("Temperatura ", self.s_dht.temperature())  # Debug
            print("Humedad  ", self.s_dht.humidity())  # Debug
            self.pin_led.value(not self.pin_led.value())  # Debug

    def tomarAccion(self):
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

    def callback(self, p):
        "Metodo que se ejecuta una vez ocurrida la interrupción"
        # print('pin change', p)
        self.sel = 0

    def loop(self):
        "Bucle principal en espera de flanco"
        # Flanco de bajada y flanco de subida rising and falling edge()
        self.p2.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.callback)
        while self.sel == 1:  # Termina por interrupción de flanco o por Pin
            # Sleep Off
            self.readData()  # Lectura de sensores
            self.saveData()  # si esta ctiva almacena datos
            # Sleep On
            time.sleep(1)
        self.saveData()


ESP8266 = Monitoreo()
ESP8266.loop()
