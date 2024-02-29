from machine import Pin
import time
 
light = Pin(25, Pin.OUT)
switch2 = Pin(14, Pin.IN, Pin.PULL_UP)

i = 1
print(i)
while True:
    if not switch2.value():
        i += 1
        print(i)
        light.value(i % 2)
        while not switch2.value():
            time.sleep(0.01)
