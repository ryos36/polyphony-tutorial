from polyphony import testbench

def mul_add(a, b, c, d):
    return a * b + c * d

@testbench
def test():
    assert 17 == mul_add(1, 2, 3, 4)
    assert 62 == mul_add(4, 5, 6, 7)

test()
