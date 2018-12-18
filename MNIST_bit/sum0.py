from polyphony import unroll, pipelined

def sum0(data):
    sum = [0] * 16
    for i in unroll(range(8)):
        sum[i] = data[i] + data[i+8]

    for i in unroll(range(4)):
        sum[i] += sum[i+4]

    for i in unroll(range(2)):
        sum[i] += sum[i+2]

    return sum[0] + sum[1]


import polyphony
from polyphony import testbench

@testbench
def test():
    rv = sum0([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    print(rv)

test()
