import dht
import machine
import time

class Monitoreo():
    def __init__(self):
        self.f = open('data.txt', 'w') 
        self.tipo_sensor1 = "DHT11"
        #self.s_dht = dht.DHT22(machine.Pin(4))
        self.sel = 1
        self.debug_mode = 1
        self.startDev()

    def startDev(self):
        self.f.write("TEMEPRATURA, HUMEDAD\n")
        self.s_dht = dht.DHT11(machine.Pin(4))
        if self.debug_mode == 1 : 
            import esp; esp.osdebug(1)  # turn on/off vendor O/S debugging messages
            self.pin_led = machine.Pin(2, machine.Pin.OUT)  # Debug visual
        else: esp.osdebug(1) 
        self.loop()

    def saveData(self):
        self.f.write(str(self.s_dht.temperature())+", "+str(self.s_dht.humidity())+"\n")

    def readData(self):
        self.s_dht.measure()
        if self.debug_mode == 1:
            print("Temperatura ", self.s_dht.temperature())  # Debug
            print("Humedad  ", self.s_dht.humidity())  # Debug
            self.pin_led.value(not self.pin_led.value())  # Debug

    def tomarAccion(self):
        pass

    def sleepMode(self):
        pass

    def wifi(self):
        pass
    
    def loop(self):
        for i in range(3):
            # Sleep Off
            self.readData()
            self.saveData()
            # Sleep On
            time.sleep(1)
        self.f.close()

ESP8266 = Monitoreo()
