import polyphony
from polyphony import module, pure
from polyphony import testbench
from polyphony.io import Port
from polyphony.typing import bit, uint32
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling

@module
class xorshift:
    def __init__(self, seed):
        self.i_start  = Port(bit, 'in')
        self.o_data  = Port(bit, 'out', protocol='valid')
        self.append_worker(self.xorshift_worker, seed, self.i_start, self.o_data)

    def xorshift_worker(self, seed, i_start, o_data):
        y:uint32 = seed
        while polyphony.is_worker_running():
            while ( 1 ):
                flag = i_start.rd()
                if flag == 1 :
                    break;
            
            y = y ^ ( y << 13 )
            y &= 0xFFFFFFFF
            y = y ^ ( y >> 17 )
            y &= 0xFFFFFFFF

            y = y ^ ( y << 5)
            y &= 0xFFFFFFFF
            rv = y
            for i in range(32):
                b:bit = rv & 1
                o_data.wr(b)
                rv = rv >> 1
            
m = xorshift(2463534242)

@testbench
def test(m):
    for i in range(10):
        rv = 0
        shift_n = 0
        b = [0] * 32
        m.i_start.wr(1)
        m.i_start.wr(0)
        for i in range(32):
            b[i] = m.o_data.rd()
        for i in range(32):
            rv = rv + (b[i] << shift_n)
            shift_n = shift_n + 1
        print("xor shift:", rv)
        clksleep(100)

test(m)
