from polyphony import testbench

dic = { 1:1, 2:4, 3:9 }
def f0(x):
    return dic[x]

@testbench
def test():
    a = f0(3)
    print(a)

test()
