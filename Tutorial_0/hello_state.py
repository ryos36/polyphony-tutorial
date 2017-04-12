from polyphony import testbench

def hello():
    i = 0
    while (i == 0):
        print("Hello World.")
        i += 1

@testbench
def test():
    hello()

test()
