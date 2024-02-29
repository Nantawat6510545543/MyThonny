from machine import Pin, I2C
# Set I2C channel 1 to Pin #4 and #5
i2c = I2C(1, sda=Pin(4), scl=Pin(5))
# Scan the I2C bus for available devices
i2c.scan()
# Specify the register address to measure the current temperature
i2c.writeto(77, bytearray([0]))
# Read two bytes and print out raw bit values
data = i2c.readfrom(77, 2)
print(f"{data[0]:08b} {data[1]:08b}")