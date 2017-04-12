from polyphony import testbench

def f0(x):
    l0 = 4 if x == 1 else 5
    return l0

@testbench
def test():
    assert 4 == f0(1) 
    assert 5 == f0(4)

test()
