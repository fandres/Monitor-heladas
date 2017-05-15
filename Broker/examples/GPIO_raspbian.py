import RPi.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)  # Entrada


while True:
    if(GPIO.input(4) ==1):
        print("Button 1 pressed")
        GPIO.output(17, True)
        sleep(1)
        GPIO.output(17, False)
    #GPIO.cleanup()
