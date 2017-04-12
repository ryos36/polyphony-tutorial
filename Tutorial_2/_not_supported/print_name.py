from polyphony import testbench

def printName(lastName, firstName, reverse):
    if reverse:
        print(firstName, lastName)
    else:
        print(lastName, ",", firstName)

@testbench
def test():
    printName("Suzuki", "Ryouzaburou", False)

test()
