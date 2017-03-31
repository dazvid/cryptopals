#!/usr/bin/python3

"""
brutexor.py

XOR a string with a single byte XOR key, and then score it
based on english character frequency.
"""

from cryptostr import int_to_hexstr, xor_strings, hexstr_to_str
from freqy import english_freq_match_score

def score_xor(message, key):
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
