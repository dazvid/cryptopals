#!/usr/bin/python3

"""
1_7.py


AES in ECB mode

The Base64-encoded content in this file has been encrypted via AES-128 
in ECB mode under the key

"YELLOW SUBMARINE".

(case-sensitive, without the quotes; exactly 16 characters; I like 
"YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do 
too).

Decrypt it. You know the key, after all.

Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.
Do this with code.

You can obviously decrypt this using the OpenSSL command-line tool, 
but we're having you get ECB working in code for a reason. You'll need 
it a lot later on, and not just for attacking ECB.
"""

#######################################
# IMPORTS
#######################################

from binascii import a2b_base64
from Crypto.Cipher import AES

#######################################
# MAIN
#######################################

with open('7.txt') as infile:
    encrypted = a2b_base64(infile.read())

key = 'YELLOW SUBMARINE'
encryptor = AES.new(key, AES.MODE_ECB)
decrypted = encryptor.decrypt(encrypted)
print(decrypted.decode('utf-8'))
