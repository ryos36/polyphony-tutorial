import polyphony
from polyphony import module, pure
from polyphony import testbench
from polyphony.io import Port
from polyphony.typing import bit, int8
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling

import sin_wave
import dac_ds

@polyphony.module
class test_dac_ds:
    def __init__(self):
        self.m_sin_wave = sin_wave.sin_wave()
        self.m_dac_ds = dac_ds.dac_ds()

    def glue_worker(self):
        self.m_dac_ds.i_port.wr(self.m_sin_wave.o_port.rd())
        self.m_dac_ds.i_detect.wr(self.m_sin_wave.o_pulse.rd())
                
m = test_dac_ds()

@testbench
def test(m):
    print("Hello")
    for i in range(100):
        clksleep(1)

test(m)
