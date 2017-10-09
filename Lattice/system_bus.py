import polyphony
from polyphony import testbench, module, is_worker_running
from polyphony.io import Port, Queue
from polyphony.typing import bit, uint8, uint3, uint4
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

        self.sbus_reset = Port(bit, 'out', init=0)
        self.sbus_ipload = Port(bit, 'out', init=0)
        self.sbus_ipdone = Port(bit, 'in')

        self.led = Port(bit, 'out')
        self.debug = Port(uint3, 'out')

        self.append_worker(self.worker)

    def write_data(self, addr:uint8, data:uint8):
        self.rw(1)
        self.addr(addr)
        self.data_out(data)
        clkfence()
        self.stb(1)
        clkfence()
        wait_value(1, self.ack)
        clkfence()
        self.stb(0)

    def read_data(self, addr:uint8):
        data:uint8 = 0
        self.rw(0)
        self.addr(addr)
        clkfence()
        self.stb(1)
        clkfence()
        wait_value(1, self.ack)
        data = self.data_in.rd()
        clkfence()
        self.stb(0)
        return data

    def read_spi_data16(self):
        debug_v:uint3 = 0

        debug_v = 4
        #self.debug.wr(4)

        self.write_data(0x06, 0x18)
        self.write_data(0x0D, 0xFF)

        while True:
            irq_status = self.read_data(0x06)
            irq_trdy = (irq_status >> 4) & 1
            if irq_trdy == 1 :
                self.write_data(0x06, 0x10)
                break
        self.write_data(0x0D, 0xFF)
        #self.debug.wr(5)

        debug_v = 1

        while True:
            irq_status = self.read_data(0x06)
            irq_rrdy = (irq_status >> 3) & 1
            debug_v = 7 ^ debug_v
        #    self.debug.wr(debug_v)
            if irq_rrdy == 1:
                self.write_data(0x06, 0x08)
                break
        data0 = self.read_data(0x0E) << 8
        debug_v = 2
        #self.debug.wr(2)

        while True:
            irq_status = self.read_data(0x06)
            irq_rrdy = (irq_status >> 3) & 1
            if irq_rrdy == 1:
                debug_v = 4 ^ debug_v
                #self.debug.wr(debug_v)
                self.write_data(0x06, 0x08)
                break
        data1 = self.read_data(0x0E)
        #self.debug.wr(1)
        return (data0 | data1)

    def worker(self):

        self.sbus_reset.wr(1) 
        clksleep(8)

        self.sbus_reset.wr(0) 
        self.sbus_ipload(1)
        
        self.debug.wr(3)
        self._wait()
        wait_value(1, self.sbus_ipdone)
        self.sbus_ipload(0)
        self.debug.wr(0)

        clksleep(8)

        self.write_data(0x07, 0x18)
        #self.write_data(0x0F, 1)
        #self.write_data(0x09, 0x80)
        #self.write_data(0x0A, 0x80)
        self.write_data(0x0B, 0x01)

        self.write_data(0x0A, 0xC0)
        self.write_data(0x0D, 0x55)
        self.debug.wr(4)

        while True:
            data = self.read_data(0x06)
            self.debug_out(data)
            if data != 0 :
                break
        self.debug.wr(2)

        self.write_data(0x0A, 0x80)

        clkfence()
        clksleep(10)

        while polyphony.is_worker_running():
            data16 = self.read_spi_data16()
            print(data16)

        #while is_worker_running():
        #    debug_v = 7 ^ debug_v
        #    self.led(1)
        #    self._wait()
        #    self.led(0)
        #    self._wait()

    def _wait(self):
        INTERVAL=20000000
        for i in range(INTERVAL):
            pass

    def debug_out(self, debug_v:uint8):
        self.debug.wr(3)
        self._wait()

        for i in range(4):
            debug_v0 = (debug_v >> ((3 - i) * 2)) & 0x3 
            if ((i & 1) == 0) :
                debug_v0 |= 4
            self.debug.wr(debug_v0)
            self._wait()

        self.debug.wr(7)
        self._wait()
        self.debug.wr(0)
        self._wait()

    def rgb_out(self, n, v0:uint3, v1:uint3):
        self.debug.wr(v0)
        self._wait()
        self.debug.wr(v1)
        self._wait()

    def debug_out0(self, debug_v:uint8):
        self.rgb_out(20, 7, 0)
        for i in range(4):
            debug_v0 = (debug_v >> i) & 0x3
            debug_v1 = debug_v0
            if ((i & 1) == 0):
                debug_v1 |= 4
            self.rgb_out(10, debug_v0, debug_v1)
        self.rgb_out(30, 7, 5)
        self.debug.wr(0)
        
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
