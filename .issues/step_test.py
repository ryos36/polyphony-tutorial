from polyphony import testbench

def step(lst_r, lst_a):
    for i in range(len(lst_a)):
        tmp = lst_a[i]
        if tmp < 0 :
            lst_r[i] = 0
        else:
            lst_r[i] = 1

def arange(lst_r, x0, sv):
    for i in range(len(lst_r)):
        lst_r[i] = x0
        x0 = x0 + sv

def test_step():
    lst_r = [0] * 101
    lst_a = [0] * 101
    print(lst_a)
    arange(lst_a, -50, 1)
    print(lst_a)
    step(lst_r, lst_a)
    print(lst_r)
        

@testbench
def test():
    test_step()

test()
