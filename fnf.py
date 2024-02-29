from machine import Pin
import time

# Define the pin connected to the relay or electronic switch
light_pin = Pin(25, Pin.OUT)

# Define the pins for the Push Buttons
switch1_pin = Pin(14, Pin.IN, Pin.PULL_UP)  # Switch1 to turn on the light
switch2_pin = Pin(16, Pin.IN, Pin.PULL_UP)  # Switch2 to turn off the light

# Function to turn on the light
def turn_on_light():
    light_pin.off()
    print("Light is ON")

# Function to turn off the light
def turn_off_light():
    light_pin.on()
    print("Light is OFF")

# Main program
i = 0
while True:
    i+=1
    print(i)
    print(switch1_pin)
    if switch1_pin.value():
        turn_off_light()
    else
        turn_on_light()
    time.sleep(0.1)