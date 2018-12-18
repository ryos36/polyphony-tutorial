from polyphony import unroll, pipelined

def sum1(data):
    sum = 0
    for i in unroll(range(16)):
        sum += data[i]

    return sum


import polyphony
from polyphony import testbench

@testbench
def test():
    rv = sum1([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    print(rv)

test()
