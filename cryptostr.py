#!/usr/bin/python3

"""
cryptostr.py

Contains a few conversions used in the cryptopals challenges.

Examples:

- bin_string:
    "test" -> "01110100011001010111001101110100"

- hamming_distance:
    s1 = "this is a test" & s2 = "wokka wokka!!!" == 37
"""

from itertools import cycle

def bin_string(s):
    "Take a string and make it a binary representation"
    return ''.join('{0:08b}'.format(ord(c)) for c in s)

def hamming_distance(s1, s2):
    "Calculate the hamming distance between two strings"
    return sum(c1 != c2 for c1, c2 in zip(bin_string(s1), bin_string(s2)))

def repeating_xor(message, key):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, cycle(key)))
