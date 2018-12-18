#from polyphony import unroll, pipelined

def sum2(data):
    sum01 = data[0] + data[1]
    sum23 = data[2] + data[3]
    sum45 = data[4] + data[5]
    sum67 = data[6] + data[7]
    sum89 = data[8] + data[9]
    sumAB = data[10] + data[11]
    sumCD = data[12] + data[13]
    sumEF = data[14] + data[15]

    sum0123 = sum01 + sum23
    sum4567 = sum45 + sum67
    sum89AB = sum89 + sumAB
    sumCDEF = sumCD + sumEF

    sum0_7 = sum0123 + sum4567
    sum8_F = sum89AB + sumCDEF

    return sum0_7 + sum8_F

import polyphony
from polyphony import testbench

@testbench
def test():
    rv = sum2([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    print(rv)

test()
