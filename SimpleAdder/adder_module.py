import polyphony
from polyphony import testbench, module
from polyphony.io import Port
from polyphony.typing import uint3, uint4
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling

@module
class adder:
    def __init__(self):
        self.i_a3  = Port(uint3, 'in', protocol='valid')
        self.i_b3  = Port(uint3, 'in', protocol='valid')
        self.o_r4  = Port(uint4, 'out', protocol='valid')
        self.append_worker(self.adder_worker)

    def adder_worker(self):
        while polyphony.is_worker_running():
            a3:uint4 = self.i_a3.rd()
            b3:uint4 = self.i_b3.rd()
            r4:uint4 = a3 + b3
            self.o_r4(r4)

m = adder()

@testbench
def test(m):
    m.i_a3.wr(3)
    m.i_b3.wr(6)
    rv = m.o_r4.rd()
    print("rv:", rv)

test(m)
