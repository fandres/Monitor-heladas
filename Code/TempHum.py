import dht
import machine
import time

class Monitoreo():
    def __init__(self):
        self.f = open('data.txt', 'w') 
        self.s_dht = dht.DHT11(machine.Pin(4))
        #self.s_dht = dht.DHT22(machine.Pin(4))
        self.sel = 1
        self.p2 = machine.Pin(3, machine.Pin.IN)
        self.debug_mode = 1
        self.startDev()

    def startDev(self):
        self.f.write("TEMEPRATURA, HUMEDAD\n")
        self.debugMode()
        self.loop()

    def debugMode(self):
        "Activa/Desactiva El debug visual y de consola"
        if self.debug_mode == 1 : 
            import esp; esp.osdebug(1)  # turn on/off vendor O/S debugging messages
            self.pin_led = machine.Pin(2, machine.Pin.OUT)  # Debug visual
        else: esp.osdebug(1) 
     
    def saveData(self):
        "Guarda los datos en un archivo"
        self.f.write(str(self.s_dht.temperature())+", "+str(self.s_dht.humidity())+"\n")

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
        print('pin change', p)
        self.sel = 0

    def loop(self):
        "Bucle principal en espera de flanco"
        # Flanco de bajada y flanco de subida rising and falling edge()
        self.p2.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.callback)
        while(self.sel == 1):  # Termina por interrupción
            # Sleep Off
            self.readData()
            self.saveData()
            # Sleep On
            time.sleep(1)
        self.f.close()


ESP8266 = Monitoreo()
