#!/usr/bin/python3

"""
2_9.py

Implement PKCS#7 padding

A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of 
plaintext into ciphertext. But we almost never want to transform a single 
block; we encrypt irregularly-sized messages.

One way we account for irregularly-sized messages is by padding, creating 
a plaintext that is an even multiple of the blocksize. The most popular 
padding scheme is called PKCS#7.

So: pad any block to a specific block length, by appending the number of 
bytes of padding to the end of the block. For instance,

"YELLOW SUBMARINE"

... padded to 20 bytes would be:

"YELLOW SUBMARINE\x04\x04\x04\x04"
"""

#######################################
# IMPORTS
#######################################

from binascii import a2b_qp
import sys

#######################################
# FUNCTIONS
#######################################

def pad_message(message, block_size):
    "Pad message to be block_size"
    fill = block_size - len(message)
    bytes_str = message.encode('utf-8')
    for _ in range(fill):
        bytes_str += fill.to_bytes(1, byteorder=sys.byteorder)
    return bytes_str.decode('utf-8')

#######################################
# MAIN
#######################################

message = 'YELLOW SUBMARINE'
block_size = 20
padded = pad_message(message, block_size)
print('Original: {} ({})\nPadded: {} ({})'.format(message, len(message),
                                                  a2b_qp(padded), len(padded)))
