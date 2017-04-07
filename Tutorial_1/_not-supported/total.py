from polyphony import testbench

def func():
    total = 0
    for i in "123456789":
        total = total + int(i)
    return total

@testbench
def test():
    result = func()
    print(result)

test()
