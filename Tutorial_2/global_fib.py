from polyphony import testbench

def fib(n):
    return n

@testbench
def test():
    test_n = [0, 46, 47, 92]
    golden_results = [ 0, 1836311903, 2971215073, 7540113804746346429]
    for i in range(len(test_n)):
        n = test_n[i]
        golden_result = golden_results[i]
        print("time:", "$time")
        result = fib(n)
        print("time:", "$time", " ",i, "=>", result)

test()
