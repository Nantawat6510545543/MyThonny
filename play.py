from machine import Pin
import uasyncio as asyncio
import network
import time
from time import sleep
from umqtt.robust import MQTTClient
from config2 import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)

sw1 = Pin(16, Pin.IN, Pin.PULL_UP)
sw2 = Pin(14, Pin.IN, Pin.PULL_UP)
lamp = Pin(25, Pin.OUT)
lamp.value(1)  # turn it off
red = Pin(2, Pin.OUT)
red.value(1)  # turn the red led off
green = Pin(12, Pin.OUT)
green.value(1)  # turn the green led off

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
print("*** Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(0.5)
print("*** Wifi connected")

mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
print("*** Connecting to MQTT broker...")
mqtt.connect()
print("*** MQTT broker connected")

timer = 0
counter = 0


async def msgR():
    while True:
        mqtt.check_msg()
        await asyncio.sleep_ms(0)


def sub_callback(topic, payload):
    global timer
    if topic.decode() == "play":
        try:
            if 1 <= int(payload) <= 5:
                if timer == 0:
                    timer = int(payload)
        except ValueError:
            pass


async def light():
    global timer
    while True:
        while timer != 0:
            red.value(0)
            await asyncio.sleep_ms(250)
            red.value(1)
            await asyncio.sleep_ms(750)
            timer -= 1
        await asyncio.sleep_ms(0)


async def count():
    global counter
    while True:
        while sw2.value() == 1:
            await asyncio.sleep_ms(0)
        await asyncio.sleep_ms(10)

        if sw2.value() == 0:
            counter += 1
            print(counter)
            mqtt.publish("play", str(counter))

        while sw2.value() == 0:
            await asyncio.sleep_ms(0)
        await asyncio.sleep_ms(10)


mqtt.set_callback(sub_callback)
mqtt.subscribe("play")

asyncio.create_task(msgR())
asyncio.create_task(light())
asyncio.create_task(count())

asyncio.run_until_complete()
