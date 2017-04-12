from polyphony import testbench

def f0(x, y):
    l0 = [1, 2, 3]
    l1 = [4, 5, 6]
    l2 = l0 + l1
    for i in l2:
        print(i)

@testbench
def test():
    a = f0(3 ,5)
    print(a)

test()
