def root_newton(x):
    epsilon = 0.001
    guess = x/2.0
    while abs(guess**2 - x) >= epsilon:
        guess = guess - (((guess**2) - x)/(2*guess))
        print(guess)

    return guess

def test():
    result = root_newton(25)
    print(result)
    result = root_newton(24)
    print(result)

test()
