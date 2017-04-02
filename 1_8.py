#!/usr/bin/python3

"""
1_8.py

Detect AES in ECB mode

In this file are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and 
deterministic; the same 16 byte plaintext block will always produce 
the same 16 byte ciphertext.
"""

#######################################
# IMPORTS
#######################################
from Crypto.Cipher import AES
import re

#######################################
# DEFINES
#######################################
BLOCK_SIZE = 16
REPEATER = re.compile(r'(.+?)\1+$')

#######################################
# FUNCTIONS
#######################################
def repeater(s):
    "Find a repeating group of chars in a string"
    match = REPEATER.match(s)
    return match.group(1) if match else None
    
#######################################
# MAIN
#######################################

with open('8.txt') as infile:
    encrypted_lines = infile.readlines()

# Filter the new line char..
encrypted_lines = [line.strip() for line in encrypted_lines]

# Search for repeating blocks of cipher text
for line in encrypted_lines:
    for i in range(len(line)):
        result = repeater(line[i:])
        if result:
            if len(result) > 1:
                print('Detected repeating chars: {}'.format(result))
                print('For line: {}'.format(line))
