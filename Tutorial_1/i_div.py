from polyphony import testbench

shift_n = 7

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

def i_bit_width(x):
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

def i_div(x, y):
    abs_x_bw = i_bit_width(x)
    abs_y_bw = i_bit_width(y)
    print("width ", abs_x_bw, abs_y_bw)
    if abs_y_bw > abs_x_bw:
        return 0
    diff_bw = abs_x_bw - abs_y_bw
    msb = (x & 0x80000000) ^ (y & 0x80000000)
    abs_x = x & 0x7FFFFFFF
    abs_y = y & 0x7FFFFFFF
    iter_x = abs_x
    iter_y = abs_y << diff_bw 
    check_bit = 1 << (abs_x_bw - 1)
    rv = 0
    print("div ", iter_x >> shift_n, abs_y, diff_bw, iter_y >> shift_n)
    for i in range(0, diff_bw + 1):
        if iter_x >= iter_y:
            print(iter_x, iter_y, 1)
        else:
            print(iter_x, iter_y, 0)

        rv <<= 1
        if iter_x >= iter_y:
            rv += 1
            iter_x -= iter_y
            if iter_x == 0:
                print("rv: ", rv)
                rv <<= (diff_bw - i)
                print("rv2: ", rv)
                break

        iter_y >>= 1
        check_bit >>= 1

    print("seisu:", rv)

    if iter_x :
        iter_x <<= shift_n
        iter_y = abs_y << (shift_n - 1)
        check_bit = 1 << (abs_y_bw + shift_n - 1)
        print("shousu:", iter_x, iter_y, check_bit)
        for i in range(0, shift_n):
            if iter_x >= iter_y:
                print(iter_x, iter_y, 1, rv)
            else:
                print(iter_x, iter_y, 0, rv)
            rv <<= 1
            if iter_x >= iter_y:
                rv += 1
                iter_x -= iter_y
                if iter_x == 0:
                    print("break rv:", (shift_n - i), rv)
                    rv <<= (shift_n - i)
                    break
            iter_y >>= 1
            check_bit >>= 1
    else:
        rv <<= shift_n

    return rv

@testbench
def test():
#    x = 255
#    y =   5
#    result = i_div(x << shift_n, y << shift_n)
#    print("result:", result)
#    print("result:", result/128)
    x = 256
    y =   5
    result = i_div(x << shift_n, y << shift_n)
    print("result:", result)
    print("result:", result/(1 << shift_n))

test()
