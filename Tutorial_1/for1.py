from polyphony import testbench

def func(x):
    for i in range(0, x):
        print(i)
        x = 5

@testbench
def test():
    func(4)

test()
