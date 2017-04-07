from polyphony import testbench

def abs(x):
    if x < 0 :
        return -x
    else:
        return x

def i_root(x):
    epsilon = 0.01
    numGuesses = 0
    step = epsilon**2
    ans = 0.0
    while abs(ans**2 - x) >= epsilon and ans <= x:
        ans += step
        numGuesses += 1
    print("numGuesses:", numGuesses)

    if abs(ans**2 - x) >= epsilon:
        return False
    else:
        return ans

@testbench
def test():
    x = 25
    result = i_root(x)
    if result :
        print(result)
    else:
        print(x, 'is not a perfect cube')

    x = 28
    result = i_root(x)
    if result :
        print(result)
    else:
        print(x, 'is not a perfect cube')

test()
