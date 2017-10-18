import polyphony
from polyphony.io import Port
from polyphony.typing import bit, uint3, uint8, uint16
from polyphony.timing import clksleep, clkfence, wait_value, wait_falling


CONVST_PULSE_CYCLE = 10
CONVERSION_CYCLE = 39

@polyphony.module
class spi_master:
    def __init__(self):
        self.sclk = Port(bit, 'out')
        self.mosi = Port(bit, 'out')
        self.miso = Port(bit, 'in')
        self.cs_n = Port(bit, 'out', init=1)

        self.data8  = Port(uint8, 'out', protocol='ready_valid')
        self.append_worker(self.worker)

    def write_data(self, data):
        self.cs_n.wr(0)
        clkfence()
        for i in range(8):
            clkfence()
            self.sclk.wr(0)

            bit1 = (data >> (7 - i)) & 1
            self.mosi.wr(bit1)
            clksleep(1)
            self.sclk.wr(1)

        self.sclk.wr(0)
        clkfence()

    def read_data(self):
        #self.cs_n.wr(0)
        #clksleep(1)

        data:uint8 = 0
        #self.sclk.wr(0)

        for i in range(8):
            data <<= 1
            clkfence()
            self.sclk.wr(1)

            clkfence()
            bit1 = self.miso.rd() & 1
            clkfence()
            self.sclk.wr(0)
            data |= bit1

        clksleep(1)
        self.cs_n.wr(1)
        return data

    def worker(self):
        #while polyphony.is_worker_running():
        self.cs_n.wr(1)
        self.sclk.wr(0)
        clksleep(1)

        self.write_data(0x34)
        data:uint8 = self.read_data()
        clksleep(1)

        self.data8.wr(data)

@polyphony.testbench
def test(spi_master):
    for i in range(7):
        wait_value(1, spi_master.sclk)
    f = 0
    for i in range(8):
        wait_value(0, spi_master.sclk)
        clkfence()
        spi_master.miso.wr(f)
        f = 1 - f
    clksleep(1)
    spi_master.miso.wr(0)
    data = spi_master.data8.rd()
    print("data0:" , data)

if __name__ == '__main__':
    spi = spi_master()
    test(spi)
