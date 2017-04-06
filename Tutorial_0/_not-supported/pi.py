from polyphony import testbench

pi = 3.14159

def func():
    return pi

@testbench
def test():
    result = func()
    print(result)

test()
