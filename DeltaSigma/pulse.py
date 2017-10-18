import math
import polyphony
from polyphony import module, pure
from polyphony import testbench
from polyphony.io import Port
from polyphony.typing import bit, int8
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling

@polyphony.module
class sin_wave:
    def __init__(self):
        self.o_port  = Port(int8, 'out', protocol='none')
        self.o_pulse  = Port(bit, 'out', protocol='none')
        self.append_worker(self.sin_wave_worker, self.o_port, self.o_pulse)

    def sin_wave_worker(self, o_port, o_pulse):
        v = 0
        while polyphony.is_worker_running():
            o_port(v)
            o_pulse.wr(1)
            print("o_pulse:", 1)
            o_pulse.wr(0)
            clksleep(1)
            v = v + 1

@polyphony.module
class dac_ds:
    def __init__(self):
        self.i_port  = Port(int8, 'in', protocol='none')
        self.i_detect  = Port(bit, 'in', protocol='none')
        self.o_data  = Port(bit, 'out', protocol='none')
        self.append_worker(self.dac_ds_worker, self.i_port, self.i_detect, self.o_data)

    def dac_ds_worker(self, i_port, i_detect, o_data):
        while polyphony.is_worker_running():
            print("dac_ds_worker")
            enable = i_detect.rd()
            #print("dac_ds_worker:enable:", enable)
            while ( enable == 0 ) :
                enable = i_detect.rd()
            v = i_port()
            o_data(v)
            print("v:", v)
                
@module
class test_dac_ds:
    def __init__(self):
        self.m_sin_wave = sin_wave()
        self.m_dac_ds = dac_ds()
        self.append_worker(self.glue_worker)

    def glue_worker(self):
        self.m_dac_ds.i_port.wr(self.m_sin_wave.o_port.rd())
        pulse_v = self.m_sin_wave.o_pulse.rd()
        print("pulse_v:", pulse_v)
        self.m_dac_ds.i_detect.wr(pulse_v)

m = test_dac_ds()

@testbench
def test(m):
    for i in range(100):
        v = m.m_dac_ds.o_data.rd()
        print("test:", v)
        clksleep(1)

test(m)
