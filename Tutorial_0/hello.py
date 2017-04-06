from polyphony import testbench

def hello():
    print("Hello World.")

@testbench
def test():
    hello()

test()
