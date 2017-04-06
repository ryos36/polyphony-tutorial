from polyphony import testbench

class BaseClass:
    def __init__(self):
        pass

    def func(self, a):
        return a * a

class MyClass_Has_A():
    def __init__(self):
        self.obj = BaseClass()

    def func(self, a):
        return self.obj.func(a)

def my_func(a):
    obj = MyClass_Has_A()
    return obj.func(a)

@testbench
def test():
    a = my_func(5)
    print(a)

test()
