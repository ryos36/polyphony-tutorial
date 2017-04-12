from polyphony import testbench

def func(x):
    y = 1
    x = x + y
    print("x = ", x, " in func")
    return x

x = 3
y = 2

@testbench
def test():
    z = func(x)

    print("z = ", z)
    print("x = ", x)
    print("y = ", y)

test()
