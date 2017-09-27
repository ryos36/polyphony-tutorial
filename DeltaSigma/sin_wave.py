import math
import polyphony
from polyphony import module, pure
from polyphony import testbench
from polyphony.io import Port
from polyphony.typing import bit, int8
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling

CONVST_PULSE_CYCLE = 10
MAX_VALUE = 127
SIN_CYCLE = 798

@pure
def sin_value(xv):
    return int(math.sin(1.0/MAX_VALUE * xv) * MAX_VALUE + 0.5)
    
@pure
def make_sin_table():
    table = [0] * SIN_CYCLE
    for i in range(SIN_CYCLE):
        v = sin_value(i)
        table[i] = sin_value(i)
    return table

table = make_sin_table()

@polyphony.module
class sin_wave:
    #@pure
    def __init__(self):
        #self.o_data = Port(int8, 'out', protocol='ready_valid')
        self.o_port  = Port(int8, 'out', protocol='none')
        self.o_pulse  = Port(bit, 'out', protocol='none')
        self.append_worker(self.sin_wave_worker, self.o_port, self.o_pulse)

    def sin_wave_worker(self, o_port, o_pulse):
        i = 0
        f = 0
        while polyphony.is_worker_running():
            v = table[i]
            clkfence()
            o_port(v)
            o_pulse(1)
            o_pulse(0)
            #print(i, ":", v)
            if i == (SIN_CYCLE-1):
                i = 0
            else:
                i = i + 1


m = sin_wave()

@testbench
def test(m):
    for i in range(100):
        print(m.o_port.rd(), ":", m.o_pulse.rd())
        clksleep(1)
    print(m.o_port.rd())

test(m)
