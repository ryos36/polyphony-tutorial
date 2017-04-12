from polyphony import testbench

shift_n = 24

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
    msb = (x & 0x80000000) ^ (y & 0x80000000)
    abs_x = x & 0x7FFFFFFF
    abs_y = y & 0x7FFFFFFF

    iter_x = abs_x
    if abs_x_bw >= abs_y_bw:
        diff_bw = abs_x_bw - abs_y_bw
        iter_y = abs_y << diff_bw 
        do_iter_n = diff_bw + 1
    else:
        diff_bw = 0
        iter_y = abs_y
        do_iter_n = 0

    print("div ", iter_x >> shift_n, abs_y, diff_bw, iter_y >> shift_n)
    for i in range(0, do_iter_n):

        rv <<= 1
        if iter_x >= iter_y:
            rv += 1
            iter_x -= iter_y
            if iter_x == 0:
                rv <<= (diff_bw - i)
                break

        iter_y >>= 1


    if iter_x :
        iter_x <<= shift_n
        iter_y = abs_y << (shift_n - 1)
        for i in range(0, shift_n):
            rv <<= 1
            if iter_x >= iter_y:
                rv += 1
                iter_x -= iter_y
                if iter_x == 0:
                    rv <<= (shift_n - i - 1)
                    break
            iter_y >>= 1
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

#131.25 25.0
    x = 256
    y =   5
    x = 25600
    y =   500
    x = 16800
    y =  3200
    x = 168
    y =  32
    x = 161
    y =  32
    x =  5
    y =  2
#    x = int(27.5625 * 256.0)
#    y = int(14.5 * 256.0)
    xshift_n = shift_n - 8
    result = i_div(x << xshift_n, y << xshift_n)
    print("result:", result)
#    print("result:", result/(1 << shift_n))

test()
