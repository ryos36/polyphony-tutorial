from polyphony import testbench

def func():
    total = 0
    for i in [1,2,3,4,5,6,7,8,9]:
        total = total + i
    return total

@testbench
def test():
    result = func()
    print(result)

test()
