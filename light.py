from machine import Pin, ADC, PWM
from time import sleep
 
light = PWM(Pin(25), freq=5000)
ain = ADC(Pin(36))
#ain.width(10)

while True:
    brightness = ain.read()
    print(brightness)
    light.duty(1023 - brightness)
    sleep(0.1)
