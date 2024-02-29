from math import log10


def ldr_to_lux(r):
    x0 = 10 ** 6
    y0 = 10
    x1 = 1
    y1 = 10 ** 6
    y = r

    x0, y0, x1, y1, y = map(log10, [x0, y0, x1, y1, y])
    m = (x0 * (y1 - y) + x1 * (y - y0)) / (y1 - y0)

    print("M: {:.4f}".format(m))
    return 10 ** m


max_V = 3.3  # V
bits = 10
R1 = 10000  # Omh
ldr_value = 496
V_a = ldr_value / (2 ** bits - 1) * max_V
I = (3.3 - V_a) / R1
R_ldr = V_a / I

print("V: {:.4f} V".format(V_a))
print("I: {:.4f} mA".format(I * 1000))
print("R_ldr: {:.4f} Omh".format(R_ldr))
print("Lux: {:.4f} Lux".format(ldr_to_lux(R_ldr)))
