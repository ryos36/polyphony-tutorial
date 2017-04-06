from polyphony import testbench

g_v = 20170406

def func():
    return g_v

@testbench
def test():
    result = func()
    print("func = ", result)

test()
