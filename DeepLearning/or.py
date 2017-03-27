from polyphony import testbench

def list_mul(lst_r, lst_a, lst_b):
    for i in range(len(lst_r)):
        lst_r[i] = lst_a[i] * lst_b[i]
    
def sum(lst):
    tmp = 0
    for i in range(len(lst)):
        tmp = tmp + lst[i]

    return tmp
    
def OR(x1, x2):
    lst_r = [0, 0]
    lst_a = [x1, x2]
    lst_b = [5, 5]
    b = -2

    list_mul(lst_r, lst_a, lst_b)
    tmp = sum(lst_r) + b

    if tmp <= 0:
        return 0
    else:
        return 1

@testbench
def test():
    print(OR(0, 0))
    print(OR(1, 0))
    print(OR(0, 1))
    print(OR(1, 1))

test()
