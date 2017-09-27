import math
import polyphony
from polyphony import module, pure
from polyphony import testbench
from polyphony.io import Port
from polyphony.typing import bit, int8
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling

CONVST_PULSE_CYCLE = 10
CONVERSION_CYCLE = 40

@polyphony.module
class ModuleTest07:
    def __init__(self):
        self.idata_a = Port(int8, 'in', protocol='valid')
        self.odata_a = Port(int8, 'out', protocol='ready_valid')
        self.append_worker(self.worker, 'foo', self.idata_a, self.odata_a)

    def worker(self, name, i, o):
        v = i()
        prod = 0
        data = [1, 2, 3, 4, 5]
        o(prod)

@testbench
def test(m):
    m.idata_a(100)


m = ModuleTest07()
test(m)
