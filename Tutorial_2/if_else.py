from polyphony import testbench

def f0(x):
    l0 = 4 if x == 1 else 5
    return l0

@testbench
def test():
    a = f0(3)
    print(a)

test()
