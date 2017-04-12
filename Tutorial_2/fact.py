from polyphony import testbench

def fact(n):
    result = 1
    while ( n > 1 ):
        result = result * n
        n -= 1
    return result

def factR(n):
    if n == 1:
        return 1
    else:
        return n * factR(n - 1)

def _factR(n, r):
    if n == 1:
        return r
    else:
        return _factR(n - 1, r * n)

def factR_tailcall(n):
    if n == 1:
        return 1
    else:
        return _factR(n - 1, n)

@testbench
def test():
    result = fact(5)
    print(result)
    #result = factR(5)
    #print(result)

    #result = factR_tailcall(5)
    #print(result)

test()
