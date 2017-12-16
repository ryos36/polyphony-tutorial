from polyphony import testbench, module, is_worker_running
from polyphony.typing import bit, bit512, bit256, bit32, uint3, uint4, List
from polyphony.io import Port, Queue
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling
from polyphony import rule
from polyphony import unroll, pipelined

k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
     0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
     0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
     0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
     0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
     0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
     0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
     0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
     0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
     0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
     0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
     0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
     0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

def bit32x8_bit256(lst:List[bit32])->bit256:
    rv256:bit256 = 0
    for i in range(8):
        rv256 <<= 32
        rv256 |= lst[i]
    return rv256

def bit32x16_bit512(lst:List[bit32])->bit512:
    rv512:bit512 = 0
    for i in range(16):
        rv512 <<= 32
        rv512 |= lst[i]
    #print('bit32->bit512', rv512, lst[15])
    #print('end start_i', start_i)
    return rv512

#def old_bit32x16_bit512(lst:List[bit32], start_i = 0)->bit512:
#    rv512:bit512 = 0
#    #print('start_i', start_i)
#    for i in range(16):
#        rv512 <<= 32
#        rv512 |= lst[start_i]
#        start_i += 1
#    print('bit32->bit512', rv512, lst[15])
#    print('end start_i', start_i)
#    return rv512

def rotr(x, y):
    #return ((x >> y) | (x << (32 - y))) & 0xFFFFFFFF
    return ((x >> y) | (x << (32 - y)))

@module
class sha256:
    def __init__(self):
        self.data_in = Queue(bit512, 'in')
        self.data_out = Queue(bit256, 'out')
        self.append_worker(self.process_sha256)

    def process_sha256(self):
        work = [0] * 64   # type: List[bit32]
        _h = [0] * 8    # type: List[bit32]
        __h = [0] * 8  # type: List[bit32]

        while is_worker_running():
            update = True

            for i in range(8):
                _h[i] = h[i]

            block_len512:bit512 = self.data_in.rd()
            block_len32 = block_len512
            count = 0
            #print(block_len512)
            #print(block_len32)

            while count < block_len32:
                #print(count, block_len32)
                count += 1
                #print("--=========")
                d512 = self.data_in.rd()
                #print("start d512 %5t", d512, "$time")
                shift_n = 480

                for i in unroll(range(16)):
                    work[i] = (d512 >> shift_n) & 0xFFFFFFFF
                    shift_n -= 32

                for i in range(16, 64):
                    wi_15 = work[i - 15]
                    s0 = rotr(wi_15, 7) ^ rotr(wi_15, 18) ^ (wi_15 >> 3)
                    wi_2 = work[i - 2]
                    s1 = rotr(wi_2, 17) ^ rotr(wi_2, 19) ^ (wi_2 >> 10)
                    wi_16 = work[i - 16]
                    wi_7 = work[i - 7]
                    work[i] = (wi_16 + s0 + wi_7 + s1) & 0xFFFFFFFF

                with rule(unroll='full'):
                    for i in range(8):
                        __h[i] = _h[i]

                for i in range(64):
                    s0 = rotr(__h[0], 2) ^ rotr(__h[0], 13) ^ rotr(__h[0], 22)
                    maj = (__h[0] & __h[1]) ^ (__h[0] & __h[2]) ^ (__h[1] & __h[2])
                    t2 = s0 + maj
                    s1 = rotr(__h[4], 6) ^ rotr(__h[4], 11) ^ rotr(__h[4], 25)
                    ch = (__h[4] & __h[5]) ^ ((~__h[4]) & __h[6])
                    t1 = __h[7] + s1 + ch + k[i] + work[i]

                    __h[7] = __h[6]
                    __h[6] = __h[5]
                    __h[5] = __h[4]
                    __h[4] = (__h[3] + t1) & 0xFFFFFFFF
                    __h[3] = __h[2]
                    __h[2] = __h[1]
                    __h[1] = __h[0]
                    __h[0] = (t1 + t2) & 0xFFFFFFFF

                with rule(unroll='full'):
                    for i in range(8):
                        _h[i] = (_h[i] + __h[i]) & 0xFFFFFFFF

            #    print("turn %5t", count, "$time")

            rv256:bit256 = 0
            with rule(unroll='full'):
                for i in range(8):
                    rv256 <<= 32
                    rv256 |= _h[i]
            #print("rv256 %5t", rv256, "$time")
            self.data_out.wr(rv256)

@testbench
def test(m):
    msg = [0x61616161] * 16 # type: List[bit32]
    lst = [0] * 16 # type: List[bit32]
    blen = len(msg)
    blocks = ((blen * 4 + 5) + 63) // 64
    print("blocks", blocks)

    start_i = 0
    m.data_in.wr(blocks)

    for i in range(blocks - 1):
        print('index:', i)
        #print('start_i', start_i)
        with rule(unroll='full'):
            for j in range(16):
                lst[j] = msg[start_i]
                start_i += 1
        rv512:bit512 = bit32x16_bit512(lst)
        print('rv512', rv512)
        m.data_in.wr(rv512)

    print("$time")

    with rule(unroll='full'):
        for i in range(16):
            lst[i] = 0

    for i in range(blen - start_i):
        lst[i] = lst[start_i]
        start_i += 1
        
    lst[blen - start_i] = 0x80000000
    lst[15] = (blocks << 8)

    v512_last:bit512 = bit32x16_bit512(lst)
    print('lastblock', v512_last)
    m.data_in.wr(v512_last)

    v256:bit256 = m.data_out.rd()
    print('sha256', v256)
    #print('R   {:032x}'.format(v256))

m=sha256()
test(m)
