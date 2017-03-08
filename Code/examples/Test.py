#2+2
3*4.0
#102**1023
print("Hi from ESP")

import machine
import time

pin = machine.Pin(2, machine.Pin.OUT)
pin.high()
pin.low()

def toggle(p):
    p.value(not p.value())
#toggle(pin)

while True:
    toggle(pin)
    time.sleep_ms(500)


