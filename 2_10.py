#!/usr/bin/python3

"""
2_10.py

Implement CBC mode

CBC mode is a block cipher mode that allows us to encrypt irregularly-sized 
messages, despite the fact that a block cipher natively only 
transforms individual blocks.

In CBC mode, each ciphertext block is added to the next plaintext 
block before the next call to the cipher core.

The first plaintext block, which has no associated previous ciphertext 
block, is added to a "fake 0th ciphertext block" called the 
initialization vector, or IV.

Implement CBC mode by hand by taking the ECB function you wrote earlier, 
making it encrypt instead of decrypt (verify this by decrypting 
whatever you encrypt to test), and using your XOR function from the 
previous exercise to combine them.

The file here is intelligible (somewhat) when CBC decrypted against 
"YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)

Don't cheat.

Do not use OpenSSL's CBC code to do CBC mode, even to verify your 
results. What's the point of even doing this stuff if you aren't going 
to learn from it?
"""

#######################################
# IMPORTS
#######################################

from cryptostr import bytes_to_hexstr, hexstr, xor_strings
from binascii import a2b_base64
from Crypto.Cipher import AES

#######################################
# FUNCTIONS
#######################################
def cbc_mode(encryptor, message, keylen, iv):
    "Implement CBC mode"
    # First block is IV ^ plain1
    # then encrypted into cipher1
    # Second block uses cipher1 ^ plain2
    # Third block uses cipher 2 ^ plain3.. etc.
    hexstr_iv = bytes_to_hexstr(iv)
    start, end = 0, keylen
    for block in range()

#######################################
# MAIN
#######################################

with open('10.txt') as infile:
    encrypted = a2b_base64(infile.read())

key = 'YELLOW SUBMARINE'
keylen = len(key)
iv = '\x00' * keylen
encryptor = AES.new(key, AES.MODE_ECB)
cbc_result = cbc_mode(encryptor, encrypted, keylen, iv)
print(cbc_result)
