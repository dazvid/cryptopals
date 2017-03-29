#!/usr/bin/python3

"""
Set 1 Challenge 2

Fixed XOR

Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

    1c0111001f010100061a024b53535009181c

    ... after hex decoding, and when XOR'd against:

    686974207468652062756c6c277320657965

    ... should produce:

    746865206b696420646f6e277420706c6179

"""

def xor_strings(xs, ys):
    return ''.join(hex(int(x, 16) ^ int(y, 16))[2:] for x, y in zip(xs, ys))

hex_string1 = '1c0111001f010100061a024b53535009181c'
hex_string2 = '686974207468652062756c6c277320657965'

print(xor_strings(hex_string1, hex_string2))
