l = [0] * 8

def sum():
    v = 0
    for i in range(len(l)):
        if (i & 1) == 0:
            v += l[i] * l[i]
    return v

gv = sum()

def set_l():
    for i in range(8):
        l[i] = i

set_l()

print(sum())
