from polyphony import testbench

#shift_n = 7
#scale_n = 128
shift_n = 30
scale_n = 1024 * 1024 * 1024

def round(x):
    return x

def abs(x):
    if x < 0 :
        return -x
    else:
        return x

def i_mul_floor(x, y):
    tmp = x * y
    return tmp >> shift_n

def i_mul_ceil(x, y):
    tmp = x * y
    d = tmp & (scale_n - 1)
    tmp >>= shift_n
    if d :
        tmp += 1
    return tmp

def i_square(x):
    return i_mul_floor(x, x)

def i_root(x):
    if x == 0 :
        return 0
    epsilon = 1
    numGuesses = 0
    new_x = x * scale_n

    low_n = 0
    if new_x > scale_n:
        high_n = new_x
    else:
        high_n = scale_n

    ans = (low_n + high_n) >> 1
    old_ans = 0
    while (abs(i_square(ans) - new_x)) >= epsilon:
        print("low = ", low_n , " high = ", high_n, " ans = ", ans)
        if old_ans == ans :
            break

        numGuesses += 1
            
        if (i_square(ans) < new_x):
            low_n = ans
        else:
            high_n = ans

        old_ans = ans
        ans = (low_n + high_n) >> 1

    return ans

@testbench
def test():
    x = 25
    result = i_root(x)
    print(result)

    x = 2
    result = i_root(x)
    print(result)

test()
