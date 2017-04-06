from polyphony import testbench

g_v0, g_v1 = 20150529, 20170406

def func():
    return g_v0

@testbench
def test():
    result = func()
    print(result)

test()
