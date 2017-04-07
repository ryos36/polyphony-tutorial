from polyphony import testbench

shift_n = 7
#shift_n = 20

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
    d = tmp & (1 << shift_n - 1)
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
    new_x = x << shift_n
    old_ans = 0
    old_diff_n = 0
    numGuesses = 0
    step = epsilon * epsilon
    ans = 0
    diff_n = - new_x 
    while diff_n < 0:
        ans += step
        numGuesses += 1
        diff_n = i_square(ans) - new_x 
        if diff_n >= 0:
            break
        old_ans = ans
        old_diff_n = diff_n

    if diff_n == 0 :
        return ans
    old_diff_n = -old_diff_n
    if old_diff_n < diff_n:
        return old_ans
    else:
        return ans

@testbench
def test():
    x = 1
    result = i_root(x)
    print(result)

    x = 2
    result = i_root(x)
    print(result)

test()
