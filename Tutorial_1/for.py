from polyphony import testbench

def func(x):
    for i in range(0, x):
        print(i)

@testbench
def test():
    func(4)
    func(10)

test()
