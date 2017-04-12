from polyphony import testbench

def f0(x):
    l0 = [i ** 2  for i in range(x)]
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
