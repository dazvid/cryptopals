#!/usr/bin/python3

def print_xor(x, y):
    print('(binary) For values x={:x} and y={:x}: {:b} ^ {:b} = {:b}'.format(x, y, x, y, x ^ y))
    print('(decimal) For values x={:x} and y={:x}: {:d} ^ {:d} = {:d}'.format(x, y, x, y, x ^ y))


print_xor(0x1b, 0xfa)
print()
print_xor(0x10, 0xf0)
print()
print_xor(0xb, 0xa)
print()
print_xor(0x1, 0xf)
