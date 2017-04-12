from polyphony import testbench

def max(x, y):
    if x > y:
        return x
    else:
        return y

@testbench
def test():
    result = max(4, 5)
    print(result)

test()
