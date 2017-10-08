import polyphony
from polyphony import testbench, module, is_worker_running
from polyphony.io import Port
from polyphony.typing import bit, uint8, uint3
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling, wait_value

CONVST_PULSE_CYCLE = 10
CONVERSION_CYCLE = 39

@polyphony.module
class system_bus:
    def __init__(self):
        self.stb = Port(bit, 'out', init=0)
        self.rw = Port(bit, 'out')
        self.addr = Port(uint8, 'out')
        self.data_out = Port(uint8, 'out')
        self.data_in = Port(uint8, 'in')
        self.ack = Port(bit, 'in')

        self.led = Port(bit, 'out')
        self.debug = Port(uint3, 'out')

        #self.append_worker(self.worker)
        self.append_worker(self.main)

    def write_data(self, addr:uint8, data:uint8):
        self.rw(1)
        self.addr(addr)
        self.data_out(data)
        self.stb(1)
        clkfence()
        wait_value(1, self.ack)
        clkfence()
        self.stb(0)

    def read_data(self, addr:uint8):
        data:uint8 = 0
        self.rw(0)
        self.addr(addr)
        self.stb(1)
        clkfence()
        wait_value(1, self.ack)
        data = self.data_in.rd()
        clkfence()
        self.stb(0)
        return data

    def read_spi_data16(self):
        self.write_data(0x06, 8)
        self.write_data(0x0D, 0xFF)
        while True:
            status = self.read_data(0x0C)
            trdy = (status >> 4) & 1
            if trdy == 1 :
                break
        self.write_data(0x0D, 0xFF)
        while True:
            irq_status = self.read_data(0x06)
            irq_rrdy = (status >> 3) & 1
            if irq_rrdy == 1:
                self.write_data(0x06, 8)
                break
        data0 = self.read_data(0x0E) << 8

        while True:
            irq_status = self.read_data(0x06)
            irq_rrdy = (status >> 3) & 1
            if irq_rrdy == 1:
                self.write_data(0x06, 8)
                break
        data1 = self.read_data(0x0E)
        return (data0 | data1)

    def worker(self):
        self.debug.wr(7)
        clksleep(10)
        self.debug.wr(1)

        #self.write_data(0x07, 8)
        #self.debug.wr(2)

        #self.write_data(0x0F, 1)
        #self.write_data(0x09, 0x80)
        #self.write_data(0x0A, 0x80)
        #self.write_data(0x0B, 11)

        #clkfence()
        #clksleep(10)
        #while polyphony.is_worker_running():
        #    data16 = self.read_spi_data16()
        #    print(data16)

        debug_v:uint3 = 7
        while is_worker_running():
            debug_v = 7 ^ debug_v
            self.debug.wr(debug_v)
            self.led(1)
            self._wait()
            self.led(0)
            self._wait()

    def _wait(self):
        INTERVAL=2000000
        for i in range(INTERVAL // 2):
            pass

    def main(self):
        led:bit = 1
        debug_v:uint3 = 7
        while is_worker_running():
            self.led(led)
            led = ~led
            debug_v = 7 ^ debug_v
            self.debug.wr(debug_v)
            self._wait()
        
@polyphony.testbench
def test(sbus):
#    sbus.ack(0)
#    for i in range(5):
#        wait_rising(sbus.stb)
#        clksleep(1)
#        sbus.ack(1)
#        clkfence()
#        sbus.ack(0)
    
    clksleep(10)

if __name__ == '__main__':
    sbus = system_bus()
    test(sbus)
