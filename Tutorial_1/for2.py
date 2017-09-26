from polyphony import testbench

def func(x):
    for j in range(0, x):
        for i in range(0, x):
            print(i)
            x = 2

@testbench
def test():
    func(4)

test()
