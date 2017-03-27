from polyphony import testbench

class BitOp:
    def __init__(self, w0, w1, b):
        self.w0 = w0
        self.w1 = w1
        self.b = b

    def eval(self, x0, x1):
        tmp0 = self.w0 * x0
        tmp1 = self.w1 * x1
        tmp = tmp0 + tmp1 + self.b
        if tmp <= 0:
            return 0
        else:
            return 1
    
def AND(x1, x2):
    op = BitOp(5, 5, -7)
    return op.eval(x1, x2)

def OR(x1, x2):
    op = BitOp(5, 5, -2)
    return op.eval(x1, x2)

def NAND(x1, x2):
    op = BitOp(-5, -5, 7)
    return op.eval(x1, x2)

def XOR(x1, x2):
    AND = BitOp(5, 5, -7)
    OR = BitOp(5, 5, -2)
    NAND = BitOp(-5, -5, 7)
    s1 = NAND.eval(x1, x2)
    s2 = OR.eval(x1, x2)
    y = AND.eval(s1, s2)
    return y

@testbench
def test():
    print(XOR(0, 0))
    print(XOR(1, 0))
    print(XOR(0, 1))
    print(XOR(1, 1))

test()
