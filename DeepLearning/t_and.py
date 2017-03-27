from polyphony import testbench

def t_mul2(t_a, t_b):
    a0, a1 = t_a
    b0, b1 = t_b
    return (a0 * b0, a1 * b0)
    
def t_sum2(t_a):
    a0, a1 = t_a
    return a0 + a1

def AND(x1, x2):
    para = (5, 5)
    b = -7

    t_r = t_mul2((x1, x2), para)
    tmp = t_sum2(t_r) + b

    if tmp <= 0:
        return 0
    else:
        return 1
    
@testbench
def test():
    print(AND(0, 0))
    print(AND(1, 0))
    print(AND(0, 1))
    print(AND(1, 1))

test()
