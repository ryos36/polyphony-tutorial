from polyphony import testbench

def arg8_mul(a, b, c, d, e, f, g, h):
    return a * b + c * d + e * f + g * h

@testbench
def test():
    a = arg8_mul(1, 2, 3, 4, 5, 6, 7, 8)
    print(a)

test()
