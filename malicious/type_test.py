from polyphony import testbench

def f(a):
    return a

def int_f(a):
    b = 3
    c = f(b)
    if c == 3:
        return a
    else:
        return b

def bool_f(a):
    b = (3 == 4)
    c = f(b)
    if c :
        return a
    else:
        return a + 3

def ib_f(a):
    if a == 1:
        return int_f(a)
    else:
        return bool_f(a)

@testbench
def test():
    #r = int_f(3) #ok
    #r = bool_f(1) #ok
    r = ib_f(1)
    print(r)

test()
