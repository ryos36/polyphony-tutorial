from polyphony import testbench

def func(str):
    print(str)

@testbench
def test():
    func("hello")

test()
