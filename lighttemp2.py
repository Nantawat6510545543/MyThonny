import time
from machine import Pin, ADC, I2C
from math import log10, pow

def get_log_slope(x1, y1, x2, y2):
    x1, y1, x2, y2 = map(log10, [x1, y1, x2, y2])
    return (y2 - y1) / (x2 - x1)

i2c = I2C(1, sda=Pin(4), scl=Pin(5))
light_sensor = ADC(Pin(36))

slope = get_log_slope(10000, 0.1, 0.1, 900)

while True:
    ldr_value = light_sensor.read()
    V_a = ldr_value / 4095 * 1.1
    R_ldr = V_a * 33 / (3.3 - V_a)
    C = log10(0.1) - slope * log10(10000)
    try:
        log_lux = (log10(R_ldr) - C) / slope
        lux = pow(10, log_lux)
    except ValueError:
        lux = 10000
    print("Light Intensity: {:.2f} Lux".format(lux))

    i2c.writeto(77, bytearray([0]))
    data = i2c.readfrom(77, 2)
    temp = (data[0] << 8) + data[1]
    temperature = temp / 128
    print("Temperature: {:.4f} °C".format(temperature))

    time.sleep(2)

