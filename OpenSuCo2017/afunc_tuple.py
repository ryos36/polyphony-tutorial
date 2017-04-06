from polyphony import testbench, module, is_worker_running
from polyphony.timing import clkfence, wait_rising, wait_value

def func_v00(t):
    (a, b) = t
    return a * b

def func_v01(a, b, c, d, e, f):
    return func_v00((a, b)) + func_v00((c, d)) + func_v00((e, f))

def func(a, b, c, d, e, f):
    v10 = func_v01(a, b, c, d, e, f)
    v11 = func_v01(b, c, d, e, f, a)

    return v10 + v11

@testbench
def test():
    r = func(1, 2, 3, 4, 5, 6)
    print(r)

test()
