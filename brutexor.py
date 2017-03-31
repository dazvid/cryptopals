#!/usr/bin/python3

"""
brutexor.py
"""

from cryptostr import int_to_hexstr, xor_strings, hexstr_to_str
from freqy import english_freq_match_score
import string

def printable_percent(s):
    "Determine the percentage of printable characters in a given string"
    printable = sum(1 for c in s if c in string.printable)
    return printable / len(s) * 100


def attempt_xor(message, key):
    "Attempt to brute force a single byte xor key"
    # generate a hex string key the same length as the encoded string
    keylen = int(len(message) / 2)
    xorkey = int_to_hexstr(key) * keylen
    result = xor_strings(message, xorkey)
    if result: result = hexstr_to_str(result)
    if result:
        #score = printable_percent(result)
        score = english_freq_match_score(result)
        return result, score
    return None, None
