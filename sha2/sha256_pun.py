def rotr(x, y):
    return '(({0} >> {1}) | ({0} << (32 - {1})))'.format(x, y)
    #return ((x >> y) | (x << (32 - y)))


def macro_expand_sha256():
    __h = [0] * 8 
    for i in range(8):
        print('_h_{0} = 0'.format(i))

    #_h = [0] * 8    # type: List[bit32]

    #--------------------------------------

    shift_n = 480
    for i in range(16):
        print('work_{0} = (d512 >> {1}) & 0xFFFFFFFF'.format(i, shift_n))
        #work[i] = (d512 >> shift_n) & 0xFFFFFFFF
        shift_n -= 32

    for i in range(16, 64):
        wi_15 = 'work_{0}'.format(i-15)
        #wi_15 = work[i - 15]

        s0 = 's0_{0}'.format(i)
        print('{0} = {1} ^ {2} ^ ({3} >> 3)'.format(s0, rotr(wi_15, 7), rotr(wi_15, 18), wi_15))
        #s0 = rotr(wi_15, 7) ^ rotr(wi_15, 18) ^ (wi_15 >> 3)

        wi_2 = 'work_{0}'.format(i-2)
        #wi_2 = work[i - 2]

        s1 = 's0_{0}'.format(i)
        print('s1 = {1} ^ {2} ^ ({3} >> 10)'.format(s1, rotr(wi_2, 17), rotr(wi_2, 19), wi_2))
        #s1 = rotr(wi_2, 17) ^ rotr(wi_2, 19) ^ (wi_2 >> 10)

        wi_16 = 'work_{0}'.format(i-16)
        #wi_16 = work[i - 16]

        wi_7 = 'work_{0}'.format(i-7)
        #wi_7 = work[i - 7]

        print('work_{0} = ({1} + {2} + {3} + {4}) & 0xFFFFFFFF'.format(i, wi_16, s0, wi_7, s1))
        #work[i] = (wi_16 + s0 + wi_7 + s1) & 0xFFFFFFFF

    for i in range(8):
        print('__h_{0} = _h_{0}'.format(i))
        #__h[i] = _h[i]

    for i in range(64):
        for j in range(8):
            __h[j] = '__h_{0}_{1}'.format(j, i)
            print(j, __h[j])
        
        s0 = '_s0_{0}'.format(i)
        print('{0} = {1} ^ {2} ^ {3}'.format(s0, rotr(__h[0], 2), rotr(__h[0], 13), rotr(__h[0], 22)))
        #s0 = rotr(__h[0], 2) ^ rotr(__h[0], 13) ^ rotr(__h[0], 22)

        maj = '_maj_{0}'.format(i)
        print('{0} = ({1} & {2}) ^ ({1} & {3}) ^ ({2} & {3})'.format(maj, __h[0], __h[1], __h[2]))
        #maj = (__h[0] & __h[1]) ^ (__h[0] & __h[2]) ^ (__h[1] & __h[2])

        t2 = '_t2_{0}'.format(i)
        print('{0} = {1} + {2}'.format(t2, s0, maj))
        #t2 = s0 + maj

        s1 = '_s1_{0}'.format(i)
        print('{0} = {1} ^ {2} ^ {3}'.format(s1, rotr(__h[4], 6), rotr(__h[4], 11), rotr(__h[4], 25)))
        #s1 = rotr(__h[4], 6) ^ rotr(__h[4], 11) ^ rotr(__h[4], 25)

        ch = '_ch_{0}'.format(i)
        print('{0} = ({1} & {2}) ^ ((~{3} & {4}))'.format(ch, __h[4], __h[5], __h[4], __h[6]))
        #ch = (__h[4] & __h[5]) ^ ((~__h[4]) & __h[6])

        t1 = '_t1_{0}'.format(i)
        print('{0} = {1} + {2} + {3} + k_{0} + work_{0}'.format(t1, __h[7], s1, ch))
        #t1 = __h[7] + s1 + ch + k[i] + work[i]

        print('{0} = {1}'.format(__h[7], __h[6]))
        #__h[7] = __h[6]

        print('{0} = {1}'.format(__h[6], __h[5]))
        #__h[6] = __h[5]

        print('{0} = {1}'.format(__h[5], __h[4]))
        #__h[5] = __h[4]

        print('{0} = ({1} + {2}) & 0xFFFFFFFF'.format(__h[4], __h[3], t1))
        #__h[4] = (__h[3] + t1) & 0xFFFFFFFF

        print('{0} = {1}'.format(__h[3], __h[2]))
        #__h[3] = __h[2]

        print('{0} = {1}'.format(__h[2], __h[1]))
        #__h[2] = __h[1]

        print('{0} = {1}'.format(__h[1], __h[0]))
        #__h[1] = __h[0]

        print('{0} = ({1} + {2}) & 0xFFFFFFFF'.format(__h[0], t1, t2))
        #__h[0] = (t1 + t2) & 0xFFFFFFFF

    lasti = 63
    for i in range(8):
        print('_h_{0} = (_h_{0} + __h_{0}_{1}) & 0xFFFFFFFF'.format(i, lasti))
        #_h[i] = (_h[i] + __h[i]) & 0xFFFFFFFF

macro_expand_sha256()
