from polyphony import testbench

def func(x):
    ans = 0
    iterLeft = x
    while ( iterLeft != 0 ):
        ans = ans + x
        iterLeft = iterLeft - 1
        if True :
            print("x = ", x, ", ans = ", ans, ", iterLeft = ", iterLeft)
    return ans

@testbench
def test():
    result = func(3)
    print(result)

test()
