from polyphony import testbench

def f0(x):
    l0 = [1, 2, 3] if x == 1 else [4, 5, 6]
    sum = 0
    for i in l0:
        sum += i
        print(i)
    return sum

@testbench
def test():
    a = f0(3)
    print(a)

test()
