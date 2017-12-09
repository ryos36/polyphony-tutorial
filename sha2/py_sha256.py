_k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
      0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
      0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
      0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
      0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
      0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
      0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
      0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
      0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
      0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
      0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
      0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
      0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
      0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
      0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
      0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

_h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
      0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

def rotr(x, y):
    return ((x >> y) | (x << (32 - y))) & 0xFFFFFFFF

def sha256(b4x16):
    w = [0] * 64
    print(b4x16)
    for i in range(16):
        w[i] = b4x16[i]

    for i in range(16, 64):
        wi_15 = w[i - 15]
        s0 = rotr(wi_15, 7) ^ rotr(wi_15, 18) ^ (wi_15 >> 3)
        wi_2 = w[i - 2]
        s1 = rotr(wi_2, 17) ^ rotr(wi_2, 19) ^ (wi_2 >> 10)
        wi_16 = w[i - 16]
        wi_7 = w[i - 7]
        w[i] = (wi_16 + s0 + wi_7 + s1) & 0xFFFFFFFF

    a, b, c, d, e, f, g, h = _h

    for i in range(64):
        s0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        t2 = s0 + maj
        s1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
        ch = (e & f) ^ ((~e) & g)
        t1 = h + s1 + ch + _k[i] + w[i]

        h = g
        g = f
        f = e
        e = (d + t1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (t1 + t2) & 0xFFFFFFFF

    _lst = [a, b, c, d, e, f, g, h]

    for i in range(8):
        _h[i] = (_h[i] + _lst[i]) & 0xFFFFFFFF

    for i in _h:
       print('{:08x}'.format(i)) 
    print("===========")

    return _h

lst = [0x61616161] * 16
sha256(lst)
lst = [0] * 16
lst[0] = 0x80000000
lst[15] = 0x00000200

rv = sha256(lst)
for i in rv:
    print('R   {:08x}'.format(i))
