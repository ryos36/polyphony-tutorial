import math
import polyphony
from polyphony import module, pure
from polyphony import testbench
from polyphony.io import Port
from polyphony.typing import bit, int8
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling

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

#table = make_sin_table()
table = [0] * SIN_CYCLE

@polyphony.module
class dac_ds:
    def __init__(self, use_sin_table = False):
        self.i_port  = Port(int8, 'in', protocol='none')
        self.i_detect  = Port(bit, 'in', protocol='none')
        self.o_data  = Port(bit, 'out', protocol='none')
        self.append_worker(self.dac_ds_worker, use_sin_table, self.i_port, self.i_detect, self.o_data)
        print("__init__")

    def dac_ds_worker(self, use_sin_table, i_port, i_detect, o_data):
        i = 0
        ti = 0
        while polyphony.is_worker_running():
            if use_sin_table : 
                v = table[ti]
                if ti == (SIN_CYCLE - 1) :
                    ti = 0
                else:
                    ti = ti + 1
            else:
                enable = self.i_detect.rd()
                while ( enable == 0 ) :
                    enable = self.i_detect.rd()
                v = self.i_port.rd()
            #print("v:", v)
                
m = dac_ds(use_sin_table = False)

@testbench
def test(m):
    print("test")
    for i in range(10):
        v = m.o_data.rd()
        print(v)
        clksleep(1)

test(m)
