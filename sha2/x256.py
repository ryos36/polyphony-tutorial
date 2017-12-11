from polyphony import testbench, module, is_worker_running
from polyphony.typing import bit, bit512, bit32, uint3, uint4, List
from polyphony.io import Port, Queue
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling

def bit32x8_bit512(lst):
    rv512:bit512
    rv512 = 0
    for i in range(8):
        rv512 <<= 32
        rv512 |= lst[i]
    return rv512

@module
class sha256:
    def __init__(self):
        self.data_in = Queue(bit512, 'in')
        self.data_out = Queue(bit512, 'out')
        self.do_digest  = Port(bit, 'in', protocol='none')
        self.do_digest_ack  = Port(bit, 'out', protocol='none')
        self.append_worker(self.process_sha256)

    def process_sha256(self):
        work = [0] * 64   # type: List[bit32]
        _h = [0] * 8    # type: List[bit32]
        __h = [0] * 8  # type: List[bit32]

        while is_worker_running():
            v512 = bit32x8_bit512(_h)
            self.data_out.wr(v512)

@testbench
def test(m):
    v512 = m.data_out.rd()
    print(v512)
#    print('R   {:08x}'.format(v512))

m=sha256()
test(m)
