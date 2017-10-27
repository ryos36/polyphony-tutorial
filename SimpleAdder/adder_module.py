import polyphony
from polyphony import testbench, module
from polyphony.io import Port
from polyphony.typing import uint3, uint4
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling

@module
class adder:
    def __init__(self):
        self.i_a3  = Port(uint3, 'in', protocol='none')
        self.i_b3  = Port(uint3, 'in', protocol='valid')
        self.o_r4  = Port(uint4, 'out', protocol='valid')
        self.append_worker(self.adder_worker)

    def adder_worker(self):
        while polyphony.is_worker_running():
            a3:uint4 = self.i_a3.rd()
            print("a3:", a3)
            b3:uint4 = self.i_b3.rd()
            r4:uint4 = a3 + b3
            self.o_r4(r4)

m = adder()

def func(m, str, v):
    print(str)
    m.i_a3.wr(v)

@testbench
def test(m):
    func(m, "hello", 4)
    m.i_a3.wr(3)
    clkfence()
    m.i_b3.wr(6)
    clkfence()
    rv = m.o_r4.rd()
    print("rv:", rv)

test(m)
