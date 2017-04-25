#!/usr/bin/python3

"""
1_3.py

Single-byte XOR cipher

The hex encoded string:

    1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt 
the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. 
Character frequency is a good metric. Evaluate each output and choose 
the one with the best score. 
"""

from hexstr import Hexstr, single_byte_xor
from isenglish import IsEnglish

if __name__ == "__main__":

    english_tester = IsEnglish()

    message = \
    '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

    hs = Hexstr(message)
    for result, key in single_byte_xor(hs):
        if result.is_printable():
            decoded = result.bytestr.decode()
            if english_tester.is_english_phrase(decoded):
                # Only need the first byte of the key..
                key = key.value[:2]
                print('(0x{}): {}'.format(key, decoded))
                break
