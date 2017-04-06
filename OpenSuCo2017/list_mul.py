from polyphony import testbench

def list_mul(lst):
    old_i = 0
    v = 0
    for i in range(len(lst)):
        if (i & 1) == 1 :
            v += lst[old_i] * lst[i]
        old_i = i

    return v

@testbench
def test():
    lst = [1, 2, 3, 4, 5, 6, 7, 8]
    a = list_mul(lst)
    print(a)

test()
