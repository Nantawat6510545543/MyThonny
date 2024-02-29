from machine import Pin
import time

# Define the pin connected to the relay or electronic switch
red = Pin(25, Pin.OUT)

# Define the pins for the Push Buttons
switch1_pin = Pin(16, Pin.IN, Pin.PULL_UP)

i = 0
while True:
    if not switch1_pin.value():
        i += 1
        print(i)
        if i % 2:
            red.value(0)
        else:
            red.value(1)
        while not switch1_pin.value():
            time.sleep(0.01)
