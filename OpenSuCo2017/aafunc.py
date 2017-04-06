from polyphony import testbench, module, is_worker_running
from polyphony.timing import clkfence, wait_rising, wait_value

def func_v00(lst, i, v):
    if len(lst) == i:
        return v
    v += lst[i] * lst[i + 1]
    return func_v00(lst, i + 2, v)

def func(a, b, c, d, e, f):
    lst = [a, b, c, d, e, f]
    v10 = func_v00(lst, 0, 0)
    v11 = func_v00(lst, 0, 0)

    return v10 + v11

@testbench
def test():
    r = func(1, 2, 3, 4, 5, 6)
    print(r)

test()
