from polyphony import testbench

shift_n = 8

def i_while(x):
    epsilon = 1
    guess = x
    old_guess = 0
    while guess > epsilon:
        if old_guess == guess :
            break;
        
        old_guess = guess 
        guess = guess - 1
        print(guess)

    return guess
        

@testbench
def test():
    x = 25
    result = i_while(x)
    print(result)

test()
