

import machine 

# Pin Entrada
#pin = machine.Pin(0)
pin = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
pin.value()

# Pin salida
pin = machine.Pin(0, machine.Pin.OUT)
# bajo
pin.value(0)
pin.low()
pin.value()
# Alto
pin.value(1)
pin.high()
pin.value()