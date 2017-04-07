from polyphony import testbench

def i_mask(x, shr_n, mask_n):
    return (x >> shr_n) & mask_n

def i_bit_width_para6(b8):
    return (b8 & 0x20, b8 & 0x10, b8 & 0x08, b8 & 0x04, b8 & 0x02, b8 & 0x01)

def i_bit_width_para7(b8):
    if b8 == 0:
        return 0
    m6 = i_bit_width_para6(b8)
    if ( b8 & 0x40 ) :
        return 7
