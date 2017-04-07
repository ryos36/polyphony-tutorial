from polyphony import testbench

def i_bit_width_prim(x, shr_n, mask_n, cmp_n, first_b):
    if x == 0:
        return 0
    b8 = first_b
    x8 = (x >> shr_n) & mask_n
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

@testbench
def test():
    x = 25
    result = i_bit_width(x)
    print(result)

    x = 0x7f
    result = i_bit_width(x)
    print(result)

    x = 0x7F000101
    result = i_bit_width(x)
    print(result)


test()
