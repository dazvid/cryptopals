#!/usr/bin/python3

"""
Convert hex to base64

The string:

    49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

    Should produce:

    SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
"""

from binascii import unhexlify, b2a_base64

def hex_to_b64(s):
    byte_string = unhexlify(s)
    return b2a_base64(byte_string).decode('utf-8')

hex_string = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

print(hex_to_b64(hex_string))
