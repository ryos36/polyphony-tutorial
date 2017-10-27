from polyphony import rule
import polyphony
from polyphony import is_worker_running
from polyphony.io import Port, Queue
from polyphony.typing import bit, uint8, uint16, uint18
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling


@polyphony.module
class Filter:
    def __init__(self):
        #self.uart = uart.Transmitter()
        #self.spi_in = AD7091R_SPIC()
        self.q = Queue(uint16, 'out', maxsize=10)
        self.din = Queue(uint16, 'in', maxsize=10)
        self.append_worker(self.proc)

    @rule(scheduling='pipeline')
    def proc(self):
        a0:uint18 = 0
        a1:uint18 = 0
        a2:uint18 = 0
        a3:uint18 = 0

        while is_worker_running():
            self.q.wr(a0 >> 2)
            data:uint16 = self.din.rd()
            a0 = a1 + data
            a1 = a2 + data
            a2 = a3 + data
            a3 =      data

            #print(data)
            #self.uart.write_hex16(data)

@polyphony.testbench
def test(m):
    datas = (0xdead, 0xbeef, 0xffff, 0x0000, 0x800)
    for data in datas:
        m.din.wr(data)
            
    for i in range(5):
        print(m.q.rd())

    clksleep(10)

if __name__ == '__main__':
    filter = Filter()
    test(filter)
