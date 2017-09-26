from polyphony import testbench

def func(x):
    new_x = x
    for j in range(0, x):
        for i in range(0, new_x):
            print(i)
            new_x = 2

@testbench
def test():
    func(4)

test()
