from machine import Pin
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


lamp = Pin(25, Pin.OUT)
lamp.value(1)  # turn USB lamp off initially


def sub_callback(topic, payload):
    # use decode instead of direct byte-array comparison
    if topic.decode() == "b6510545543/lamp":
        try:
            wait = int(payload)
            if 1 <= wait <= 10:
                lamp.value(0) 
                sleep(wait)
                lamp.value(1)
            else:
                print("invalid wait time")
        except ValueError:
            pass
    
mqtt.set_callback(sub_callback)
mqtt.subscribe("b6510545543/lamp")


while True:
    mqtt.check_msg()

