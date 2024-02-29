from machine import Pin, ADC
from time import sleep

ain = ADC(Pin(36))

while True:
    inp = ain.read()
    va = (3.9 / 2 ** 12) * inp
    i = (3.3 - va) / (33 * (10 ** 3))
    ldr = va / i
    print(ldr)
    sleep(1)
