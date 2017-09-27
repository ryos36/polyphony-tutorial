import math
import polyphony
from polyphony import module, pure
from polyphony import testbench
from polyphony.io import Port
from polyphony.typing import bit, int8
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling

import sin_wave

MAX_VALUE = 127
SIN_CYCLE = 798

@polyphony.module
class dac_ds:
    def __init__(self):
        self.i_port  = Port(int8, 'in', protocol='none')
        self.i_detect  = Port(bit, 'in', protocol='none')
        self.append_worker(self.dac_ds_worker, self.i_port, self.i_detect)

    def sin_wave_worker(self, i_port, i_detect):
        while polyphony.is_worker_running():
            enable = i_detect.rd()
            while ( enable == 1 ) :
                v = i_port.rd()
                
m = sin_wave()

@testbench
def test(m):
    for i in range(100):
        print(m.o_port.rd(), ":", m.o_pulse.rd())
        clksleep(1)
    print(m.o_port.rd())

test(m)
