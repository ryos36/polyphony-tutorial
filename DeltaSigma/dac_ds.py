import math
import polyphony
from polyphony import module, pure
from polyphony import testbench
from polyphony.io import Port
from polyphony.typing import bit, int8
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling

#import sin_wave

@polyphony.module
class dac_ds:
    def __init__(self):
        self.i_port  = Port(int8, 'in', protocol='none')
        self.i_detect  = Port(bit, 'in', protocol='none')
        self.o_data  = Port(bit, 'out', protocol='none')
        self.append_worker(self.dac_ds_worker, self.i_port, self.i_detect, self.o_data)

    def dac_ds_worker(self, i_port, i_detect, o_data):
        while polyphony.is_worker_running():
            enable = i_detect.rd()
            while ( enable == 0 ) :
                enable = i_detect.rd()
            v = i_port.rd()
            print("v:", v)
                
m = dac_ds()

#def do_one(v):
#    module.i_port.wr(v)
#    module.i_detect.wr(1)
#    module.i_detect.wr(0)

@testbench
def test(m):
    #do_one(123)
    m.i_port.wr(12)
    m.i_detect.wr(1)
    m.i_detect.wr(0)
    m.i_port.wr(123)
    m.i_detect.wr(1)
    m.i_detect.wr(0)

test(m)
