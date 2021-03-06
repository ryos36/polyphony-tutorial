from polyphony import testbench

def cube(x):
    return x * x * x

def abs(x):
    if x < 0 :
        return -x
    else:
        return x

def cubic_root(x):
    ans = 0
    while cube(ans) < abs(x):
        ans = ans + 1
    if cube(ans) != abs(x):
        return False
    else:
        if x < 0 :
            ans = -ans
        return ans

@testbench
def test():
    x = 27
    result = cubic_root(x)
    if result :
        print(result)
    else:
        print(x, 'is not a perfect cube')

    x = 28
    result = cubic_root(x)
    if result :
        print(result)
    else:
        print(x, 'is not a perfect cube')

test()
