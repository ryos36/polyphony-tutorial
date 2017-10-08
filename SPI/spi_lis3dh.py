import polyphony
from polyphony.io import Port
from polyphony.typing import bit, uint3, uint12, uint24
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling


CONVST_PULSE_CYCLE = 10
CONVERSION_CYCLE = 39

@polyphony.module
class spi_lis3dh:
    def __init__(self):
        self.sclk = Port(bit, 'out')
        self.mosi = Port(bit, 'out')
        self.miso = Port(bit, 'in')
        self.cs_n = Port(bit, 'out', init=1)

        self.x_led = Port(bit, 'out')
        self.y_led = Port(bit, 'out')
        self.z_led = Port(bit, 'out')

        self.data24  = Port(uint24, 'out', protocol='ready_valid')
        self.append_worker(self.worker)

    def set_addr(self, rw, ms, addr):
        clksleep(1)
        self.sclk.wr(0)
        self.mosi.wr(rw)

        clksleep(2)
        self.sclk.wr(1)

        clksleep(2)
        self.sclk.wr(0)
        self.mosi.wr(ms)

        clksleep(2)
        self.sclk.wr(1)

        clksleep(2)
        self.sclk.wr(0)

        for i in range(6):
            bit1 = (addr >> (5 - i)) & 1
            self.mosi.wr(bit1)
            clksleep(1)
            self.sclk.wr(1)

            clksleep(1)
            self.sclk.wr(0)

        clksleep(1)

    def read_data(self, addr):
        self.cs_n.wr(0)
        self.sclk.wr(0)
        clksleep(1)

        self.set_addr(1, 0, addr)
        data = 0

        for i in range(8):
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

    def write_data(self, addr, data):
        self.cs_n.wr(0)
        self.sclk.wr(0)
        clksleep(1)

        self.set_addr(0, 0, addr)

        for i in range(8):
            bit1 = (data >> (7 - i)) & 1
            self.mosi.wr(bit1)
            clksleep(1)
            self.sclk.wr(1)

            clksleep(1)
            self.sclk.wr(0)

        clksleep(2)
        self.cs_n.wr(1)
        self.mosi.wr(0)
        return data

    def worker(self):
        self.cs_n.wr(1)
        self.sclk.wr(0)
        clksleep(1)

        self.write_data(0x20, 0x7F)
        while polyphony.is_worker_running():
            clksleep(20)

            self.write_data(0x20, 0x7F)
            clksleep(10)

            data_who_am_i = self.read_data(0x0F)
            clksleep(10)

            data_x_l = self.read_data(0x29)
            clksleep(10)

            data_y_l = self.read_data(0x2B)
            clksleep(10)

            data_z_l = self.read_data(0x2D)
            clksleep(10)

            self.x_led.wr(1 if data_x_l > 0x30 else 0)
            self.y_led.wr(1 if data_y_l > 0x30 else 0)
            self.z_led.wr(1 if data_z_l > 0x30 else 0)

            data_xyz = ( data_x_l << 16 ) | ( data_y_l << 8 ) | data_z_l
            self.data24.wr(data_xyz)

@polyphony.testbench
def test(spic):
    data = spic.data24.rd()
    print("data0:" , data)
    data = spic.data24.rd()
    print("data1:" , data)

if __name__ == '__main__':
    spic = spi_lis3dh()
    test(spic)
