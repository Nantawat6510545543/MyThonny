from machine import Pin
import uasyncio as asyncio

import network
import time
from time import sleep
from umqtt.robust import MQTTClient
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)


lamp = Pin(25, Pin.OUT)
lamp.value(1)  # turn it off


led_wifi = Pin(2, Pin.OUT)
led_wifi.value(1)  # turn the red led off
led_iot = Pin(12, Pin.OUT)
led_iot.value(1)   # turn the green led off


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    time.sleep(0.5)
led_wifi.value(0)  # turn the red led on


mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
mqtt.connect()
led_iot.value(0)   # turn the green led on


sw1 = Pin(16, Pin.IN, Pin.PULL_UP)
lamp = Pin(25, Pin.OUT)
lamp.value(1)  # turn USB lamp off initially

async def msgR():
    while True:
        mqtt.check_msg()
        await asyncio.sleep_ms(0)


def sub_callback(topic, payload): 
    if topic.decode() == "b6510545543/lamp/sw":
        try:
            lamp.value(int(payload) ^ 1)
        except ValueError:
            pass
            
async def ledTogle():
    lamp.value(1)
    while True: 
        while sw1.value() == 1:
            await asyncio.sleep_ms(0)
        lv = 1 - lamp.value()
        mqtt.publish("b6510545543/lamp/sw", str(lv ^ 1)) 
        lamp.value(lv)
        await asyncio.sleep_ms(10) 
        while sw1.value() == 0:
            await asyncio.sleep_ms(0)
        await asyncio.sleep_ms(10)


mqtt.set_callback(sub_callback)
mqtt.subscribe("b6510545543/lamp/sw")

asyncio.create_task(msgR())
asyncio.create_task(ledTogle()) 

asyncio.run_until_complete()



