

# Exepto Pin 16
from machine import Pin

pin = Pin(2, Pin.OUT)


def callback(p):
    print('pin change', p)
    pin.value(not pin.value())
    
    
# Pines Entrada
p0 = Pin(0, Pin.IN) 
p2 = Pin(3, Pin.IN)

# Interrupción 
# flanco bajada (falling edge)
p0.irq(trigger=Pin.IRQ_FALLING, handler=callback)
# Flanco de bajada y flanco de subida rising and falling edge()
p2.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)