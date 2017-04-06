from polyphony import testbench

class BaseClass:
    def __init__(self):
        pass

    def func(self, a):
        return a * a

class MyClass_Is_A(BaseClass):
    def __init__(self):
        pass

def my_func(a):
    obj = MyClass_Is_A()
    return obj.func(a)

@testbench
def test():
    a = my_func(5)
    print(a)

test()
