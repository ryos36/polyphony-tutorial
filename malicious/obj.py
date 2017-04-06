from polyphony import testbench

class MyClass:
    def __init__(self, a = 0):
        self.a = a

#    @ignore
#    def __str__(self):
#        return "a:{}".format(self.a)

    def my__add__(self, other):
        return self.a + other.a 

def myadd(c, a0, a1):
    x0 = MyClass(a0)
    x1 = MyClass()

#   return x0 + x1
    return x0.my__add__(x1) 


@testbench
def test():
    print(myadd(1, 4, 5))
    print(myadd(2, 4, 5))

test()
