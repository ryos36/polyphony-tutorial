from polyphony import testbench

shift_n = 7

def i_bit_width(x):
    if 8 == 0:
        return 0
    
    cmp_bit = 0x40000000
    for i in range(1, 31):
        if x & cmp_bit:
            return 32 - i
        cmp_bit >>= 1
    return 0

def i_div(x, y):
    #abs_x_bw = i_bit_width(x)
    abs_y_bw = i_bit_width(y)
    return 0

@testbench
def test():
    x = 640
    y =   5
    print(i_bit_width(x)) 
    print(i_bit_width(y)) 
    result = i_div(x << shift_n, y << shift_n)
    print("result:", result)
#    print("result:", result/(1 << shift_n))

test()
