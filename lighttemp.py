import time
from machine import Pin, ADC, I2C
from math import log10, pow

i2c = I2C(1, sda=Pin(4), scl=Pin(5))
light_sensor = ADC(Pin(36))


def linterp(x0, y0, x1, y1, y):
    x0, y0, x1, y1,y = map(log10, [x0, y0, x1, y1, y])
    return (x0 * (y1 - y) + x1 * (y - y0)) / (y1 - y0)


def ldr_to_lux(r):
    result = linterp(10000, 0.1, 0.1, 900,  log10(r))
    return 10 ** result


while True:
    ldr_value = light_sensor.read()
    V_a = ldr_value / 4095 * 1.1
    R_ldr = V_a * 33000/ (3.3 - V_a)
    print(R_ldr)
    lux = ldr_to_lux(R_ldr)
    print("Light Intensity: {:.2f} Lux".format(lux))

    i2c.writeto(77, bytearray([0]))
    data = i2c.readfrom(77, 2)
    temp = (data[0] << 8) + data[1]
    temperature = temp / 128
    print("Temperature: {:.4f} °C".format(temperature))

    time.sleep(2)
