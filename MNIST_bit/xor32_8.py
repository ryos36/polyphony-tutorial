import polyphony
from polyphony import testbench
from polyphony.typing import List, bit32, bit8, bit6, bit4, bit
from polyphony import unroll

from xor32_8_data import DATA_W, DATA_th
from count_table import xbit4_to_n

def count_bit32(x:bit32)->bit6:
    mask:bit32 = 0xF
    shift_n = 0
    sum = 0
    for i in unroll(range(8)):
        sum += xbit4_to_n[((x & mask) >> shift_n)]
        mask <<= 4
        shift_n += 4

    return sum

def nn_xor32_8(x:bit32)->bit8:
    rv_xor8:bit8 = 0
    for wi in unroll(range(len(DATA_W))):
        tmp_x:bit6 = count_bit32(x ^ DATA_W[wi])

        rv_xor8 <<= 1
        rv_xor8 |= 0 if tmp_x < DATA_th[wi] else 1

    return rv_xor8
        
@testbench        
def test():
    rv = nn_xor32_8(0x32)
    print(rv)
    #print('{:08x}'.format(rv))

test()
