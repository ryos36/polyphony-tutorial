import polyphony
from polyphony import module, pure
from polyphony import testbench
from polyphony.io import Port
from polyphony.typing import bit, uint3, uint4, List
from polyphony.timing import clksleep, clkfence, wait_rising, wait_falling



@module
class life:
    def __init__(self):
        self.i_bit4  = Port(uint4, 'in', protocol='valid')
        self.o_bit  = Port(bit, 'out', protocol='valid')
        self.append_worker(self.life_worker, self.i_bit4, self.o_bit)

    def life_worker(self, i_bit4, o_bit):
        bit3_to_n = [ 0, 1, 1, 2, 1, 2, 2, 3 ]
        bit3_to_m = [ 0, 1, 0, 1, 1, 2, 1, 2 ] 
        n_to_o = [0, 0, 1, 1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0] 
        mat = [0] * 3 # 

        while polyphony.is_worker_running():
            v = i_bit4()
            #print("mat", mat)
            #print("v", v)
            if v == 8 : 
                mat2_old = mat[2]
                mat[0] = 0
                mat[1] = 0
                mat[2] = 0
            else:
                v0 = bit3_to_n[v]
                v1 = bit3_to_m[v]
                mat0_old = mat[0]
                mat1_old = mat[1]
                mat2_old = mat[2]
                mat[0] = 16 + v0
                mat[1] = mat0_old + v1
                mat[2] = mat1_old + v0
            #print("mat2_old:", mat2_old)
            if (mat2_old & 16) == 16 :
                out_v = n_to_o[mat2_old & 15]
                o_bit.wr(out_v)

m = life()

@testbench
def test(m):
    m.i_bit4.wr(0)
    clksleep(5)
    m.i_bit4.wr(0)
    clksleep(5)
    m.i_bit4.wr(1)
    v = m.o_bit.rd()
    clksleep(5)

    if 1 :
        m.i_bit4.wr(0)
        clksleep(5)
        print("outv:", v)

    if 0:
        m.i_bit4.wr(0)
        clksleep(5)
        v = m.o_bit.rd()
        print("outv:", v)

    if 0 :
        m.i_bit4.wr(4)
        v = m.o_bit.rd()
        print("outv:", v)

        m.i_bit4.wr(3)
        v = m.o_bit.rd()
        print("outv:", v)

        m.i_bit4.wr(0)
        v = m.o_bit.rd()
        print("outv:", v)

        m.i_bit4.wr(0)
        v = m.o_bit.rd()
        print("outv:", v)

        m.i_bit4.wr(8)
        v = m.o_bit.rd()
        print("outv:", v)

        print("-")
        clksleep(10)
        #
        m.i_bit4.wr(0)
        m.i_bit4.wr(0)
        m.i_bit4.wr(2)

        m.i_bit4.wr(1)
        v = m.o_bit.rd()
        print("outv:", v)

        m.i_bit4.wr(1)
        v = m.o_bit.rd()
        print("outv:", v)

        m.i_bit4.wr(1)
        v = m.o_bit.rd()
        print("outv:", v)

        m.i_bit4.wr(7)
        v = m.o_bit.rd()
        print("outv:", v)

        m.i_bit4.wr(0)
        v = m.o_bit.rd()
        print("outv:", v)

        m.i_bit4.wr(0)
        v = m.o_bit.rd()
        print("outv:", v)

        m.i_bit4.wr(8)
        v = m.o_bit.rd()
        print("outv:", v)


test(m)
