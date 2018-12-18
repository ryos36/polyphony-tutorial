from polyphony import testbench, module, is_worker_running
from polyphony.timing import clksleep
from polyphony.io import Port
from polyphony.typing import bit, bit8, bit23, bit24, bit25, bit32
from polyphony.typing import int24

OP_MINUS:bit = 1
OP_ADD:bit = 1

def float32_to_bit(a:bit32):
    a_sign:bit = (a >> 31) & 0x1
    a_exp:bit8 = (a >> 23) & 0xFF
    a_fract:bit24 = a & 0x3FFFF | 0x40000
    return (a_sign, a_exp, a_fract)

def bit_to_float32(a_sign:bit32, a_exp:bit32, a_fract:bit32)->bit32:
    return (a_sign << 31) | (a_exp << 23) | a_fract

def float32_plus(a, b):
    print('flo', a, b)
#    a_sign:bit = (a >> 31) & 0x1
#    a_exp:bit8 = (a >> 23) & 0xFF
#    a_fract:bit23 = a & 0x3FFFF
#    b_sign:bit = (b >> 31) & 0x1
#    b_exp:bit8 = (b >> 23) & 0xFF
#    b_fract:bit23 = b & 0x3FFFF
    (b_sign, b_exp, b_fract) = float32_to_bit(b)
    (a_sign, a_exp, a_fract) = float32_to_bit(a)
    print(a_exp, b_exp)
    print(a_fract & 0x3FFFF, b_fract & 0x3FFFF)

    an_op:bit = a_sign ^ b_sign

    if a_exp > b_exp:
        (a_sign, b_sign) = (b_sign, a_sign)
        (a_exp, b_exp) = (b_exp, a_exp)
        (a_fract, b_fract) = (b_fract, a_fract)

    if a_exp != b_exp:
        a_fract >>= (b_exp - a_exp)
        #comment: a_exp = b_exp

    rv_fract:bit24
    if an_op == OP_MINUS:
        if a_fract < b_fract:
            rv_fract = b_fract - a_fract
        else:
            rv_fract = a_fract - b_fract
            b_sign = a_sign
    else:
        fract:bit25 = a_fract + b_fract
        print('PLUS', fract & 0x3FFFF)
        if fract & 0x80000:
            ca = fract & 1
            fract = fract >> 1
            b_exp += 1
            if ca:
                fract += 1
                if fract & 0x80000:
                    fract = fract >> 1
                    b_exp += 1
        rv_fract = fract

    return bit_to_float32(b_sign, b_exp, rv_fract & 0x3FFFF)
        
@testbench        
def test():
    a:bit32 = bit_to_float32(0, 2, 3)
    b:bit32 = bit_to_float32(0, 2, 4)
    #a:bit32 = (2 << 23) + 3
    #b:bit32 = (2 << 23) + 4
    print(a, b)
    
    rv = float32_plus(a, b)

    #print(rv)
    #(rv_sign, rv_exp, rv_fract) = float32_to_bit(rv)
    rv_sign:bit = (rv >> 31) & 0x1
    rv_exp:bit8 = (rv >> 23) & 0xFF
    rv_fract:bit23 = rv & 0x3FFFF
    print(rv_sign, rv_exp, rv_fract)
    #print(float32_to_bit(rv))
    
test()
