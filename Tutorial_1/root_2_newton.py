from polyphony import testbench

shift_n = 8
#shift_n = 30

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

def i_bit_width_prim(x, shr_n, mask_n, cmp_n, first_b):
    b8 = first_b
    x8 = (x >> shr_n) & mask_n
    if x8 == 0:
        return 0
    for i in range(cmp_n, 0, -1):
        if b8 & x8:
            return i + shr_n
        b8 >>= 1
    return 0

def i_bit_width0(x):
    r76 = i_bit_width_prim(x, 24, 0x7F, 7, 0x40)
    r54 = i_bit_width_prim(x, 16, 0xFF, 8, 0x80)
    r32 = i_bit_width_prim(x,  8, 0xFF, 8, 0x80)
    r10 = i_bit_width_prim(x,  0, 0xFF, 8, 0x80)

    #print(r76, r54, r32, r10)
    if r76 != 0:
        return r76
    elif r54 != 0:
        return r54
    elif r32 != 0:
        return r32
    else:
        return r10

def i_bit_width(x):
    if 8 == 0:
        return 0
    
    cmp_bit = 0x40000000
    for i in range(1, 31):
        if x & cmp_bit:
            return 32 - i
        cmp_bit >>= 1
    return 0

def i_div(x, y):
    abs_x_bw = i_bit_width(x)
    abs_y_bw = i_bit_width(y)
    rv = 0
    if abs_y_bw > abs_x_bw:
        return 0
    diff_bw = abs_x_bw - abs_y_bw
    msb = (x & 0x80000000) ^ (y & 0x80000000)
    abs_x = x & 0x7FFFFFFF
    abs_y = y & 0x7FFFFFFF
    iter_x = abs_x
    iter_y = abs_y << diff_bw 
    check_bit = 1 << (abs_x_bw - 1)
    #print("div ", iter_x >> shift_n, abs_y, diff_bw, iter_y >> shift_n)
    for i in range(0, diff_bw + 1):

        rv <<= 1
        if iter_x >= iter_y:
            rv += 1
            iter_x -= iter_y
            if iter_x == 0:
                rv <<= (diff_bw - i)
                break

        iter_y >>= 1
        check_bit >>= 1


    if iter_x :
        iter_x <<= shift_n
        iter_y = abs_y << (shift_n - 1)
        check_bit = 1 << (abs_y_bw + shift_n - 1)
        for i in range(0, shift_n):
            rv <<= 1
            if iter_x >= iter_y:
                rv += 1
                iter_x -= iter_y
                if iter_x == 0:
                    rv <<= (shift_n - i)
                    break
            iter_y >>= 1
            check_bit >>= 1
    else:
        rv <<= shift_n

    return rv

def i_square(x):
    return i_mul_floor(x, x)

def i_root(x):
    if x == 0 :
        return 0
    epsilon = 1
    numGuesses = 0
    new_x = x << shift_n

    guess = new_x >> 1
    old_guess = 0
    while (abs(i_square(guess) - new_x)) >= epsilon:
        print("numGuesses = ", numGuesses, " guess = ", guess)
        if old_guess == guess :
            break

        numGuesses += 1
            
        old_guess = guess
        print("i_div = ", guess , (i_square(guess) - new_x), (2*guess), i_div((i_square(guess) - new_x),(2*guess)))
        guess = guess - i_div((i_square(guess) - new_x),(2*guess))

    return guess

@testbench
def test():
    x = 25
    new_x = x << shift_n
    guess = new_x >> 1
    print("doko", i_square(guess)/(1<<shift_n), new_x/(1<<shift_n), (2*guess)/(1<<shift_n))
    print("sonde?:", (i_square(guess) - new_x)/(1<<shift_n), (2*guess)/(1<<shift_n))
    print("sorede?:", (((i_square(guess) - new_x)/(2*guess))))
    print("xsorede?:", i_div((i_square(guess) - new_x),(2*guess))/(1<<shift_n))
    print(i_square(guess) - new_x)
    print((i_square(guess) - new_x)/(1<<shift_n))
    print("1?:", (guess - (((i_square(guess) - new_x)/(2*guess)))) / (1<<shift_n))

    guess = 25.0/2.0
    print((guess**2), x)
    print((guess**2) - x)
#    result = i_root(x)
#    print(result)

#    x = 2
#    result = i_root(x)
#    print(result)

test()
