from polyphony import testbench, module, is_worker_running
from polyphony.timing import clkfence, wait_rising, wait_value

def arg8_mul(a, b, c, d, e, f, g, h):
    return a * b + c * d + e * f + g * h

def func(a, b, c, d, e, f, g, h):
    v10 = arg8_mul(a, b, c, d, e, f, g, h)
    v11 = arg8_mul(h, a, b, c, d, e, f, g)

    return v10 + v11

@testbench
def test():
    r = func(1, 2, 3, 4, 5, 6, 7, 8)
    print(r)

test()
