import polyphony
from polyphony.io import Port
from polyphony.typing import bit, uint3, uint12, uint16
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling


CONVST_PULSE_CYCLE = 10
CONVERSION_CYCLE = 39

@polyphony.module
class pmod_als:
    def __init__(self):
        self.sclk = Port(bit, 'out')
        self.miso = Port(bit, 'in')
        self.cs_n = Port(bit, 'out', init=1)

        self.data16  = Port(uint16, 'out', protocol='ready_valid')
        self.append_worker(self.worker)

    def read_data(self):
        self.cs_n.wr(0)
        clksleep(1)

        data:uint16 = 0
        self.sclk.wr(0)

        for i in range(16):
            data <<= 1
            clksleep(1)
            self.sclk.wr(1)

            clksleep(1)
            bit1 = self.miso.rd() & 1
            clkfence()
            self.sclk.wr(0)
            data |= bit1

        clksleep(1)
        self.cs_n.wr(1)
        return data

    def worker(self):
        while polyphony.is_worker_running():
            self.cs_n.wr(1)
            self.sclk.wr(0)
            clksleep(1)

            data:uint16 = self.read_data()
            clksleep(1)

            self.data16.wr(data)

@polyphony.testbench
def test(spic):
    data = spic.data16.rd()
    print("data0:" , data)
    data = spic.data16.rd()
    print("data1:" , data)

if __name__ == '__main__':
    spic = pmod_als()
    test(spic)
