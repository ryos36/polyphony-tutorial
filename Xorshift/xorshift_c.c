#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

uint32_t
xorshift(void)
{
    static uint32_t y = 2463534242;

    y = y ^ (y << 13);
    y = y ^ (y >> 17);

    y = y ^ (y << 5);
    return y;
}

int
main(int argc, char **argv)
{
    uint32_t a;
    int i;
    uint32_t n = (argc == 2)?atoi(argv[1]):1;
    for( i = 0 ; i < n ; i++ ) {
        a = xorshift();
        printf("%u\n", a);
    }
    return 0;
}
