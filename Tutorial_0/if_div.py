from polyphony import testbench

g_v0 = 20150529
g_v1 = 20170406

def func(n):
    if n % 2:
        return g_v0
    else:
        return g_v1

@testbench
def test():
    result = func(0)
    print(result)
    result = func(1)
    print(result)

test()
