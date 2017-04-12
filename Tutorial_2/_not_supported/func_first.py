from polyphony import testbench

def h0(x):
    return x * x

def h1(x):
    return - x * x

def g0(f, x):
    return f(x)

def f0(x):
    return g0(h1 if x < 0 else h0, x)


@testbench
def test():
    a = f0(3)
    print(a)

test()
