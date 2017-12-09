from polyphony import testbench

_h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
      0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

def list_test():
      a, b, c, d, e, f, g, h = _h
      #l = [0] * 64
      #l = a, b, c, d, e, f, g, h
      return a + b


@testbench
def test():
    rv = list_test()
    print(rv)

test()
