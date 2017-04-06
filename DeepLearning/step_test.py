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

def sum(lst):
    s = 0
    for i in range(len(lst)):
        #a = lst[i]
        #s = s + a * a
        s = s + lst[i] * lst[i]
    return s

def step_test(r):
    lst_r = [0] * 101
    lst_a = [0] * 101
    s = sum(lst_a)
    r[0] = s
    arange(lst_a, -50, 1)
    s = sum(lst_a)
    r[1] = s
    step(lst_r, lst_a)
    s = sum(lst_r)
    r[2] = s
    return sum(r)

@testbench
def test():
    r = [0] * 3
    tmp = step_test(r)
    print(tmp)
    tmp = step_test(r)
    print(tmp)

test()
