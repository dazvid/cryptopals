#!/usr/bin/python3

"""
Convert hex to base64

The string:

    49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

    Should produce:

    SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
"""

import binascii

def hex_to_b64(s):
    byte_string = binascii.unhexlify(s)
    string_b64 = binascii.b2a_base64(byte_string).decode('utf-8')
    return string_b64

hex_string = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

print(hex_to_b64(hex_string))
