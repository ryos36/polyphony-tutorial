from polyphony import testbench

def t0(x, y):
    return (1 if (x == 1) else 0, x-y, x+y)

def f0(x, y):
    (a, b, c) = t0(x, y)
    if a:
        return b
    else:
        return c

@testbench
def test():
    a = f0(3 ,5)
    print(a)

test()
