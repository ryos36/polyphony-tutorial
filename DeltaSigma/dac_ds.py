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

table = make_sin_table()

@polyphony.module
class dac_ds:
    def __init__(self, use_sin_table = False):
        self.i_port  = Port(int8, 'in', protocol='none')
        self.i_detect  = Port(bit, 'in', protocol='none')
        self.o_data  = Port(bit, 'out', protocol='none')
        self.append_worker(self.dac_ds_worker, use_sin_table, self.i_port, self.i_detect, self.o_data)

    def dac_ds_worker(self, use_sin_table, i_port, i_detect, o_data):
        i = 0
        while polyphony.is_worker_running():
            if use_sin_table : 
                v = table[i]
                if i == (SIN_CYCLE - 1) :
                    i = 0
                else:
                    i = i + 1
            else:
                enable = i_detect.rd()
                while ( enable == 0 ) :
                    enable = i_detect.rd()
                v = i_port.rd()
            print("v:", v)
                
m = dac_ds(use_sin_table = True)

@testbench
def test(m):
    print("test")
    for i in range(800):
        v = m.o_data.rd()
        print(v)
        clksleep(1)

test(m)
