#!/usr/bin/python3

"""
2_10.py

Implement CBC mode

CBC mode is a block cipher mode that allows us to encrypt irregularly-sized 
messages, despite the fact that a block cipher natively only transforms 
individual blocks.

In CBC mode, each ciphertext block is added to the next plaintext block 
before the next call to the cipher core.

The first plaintext block, which has no associated previous ciphertext 
block, is added to a "fake 0th ciphertext block" called the initialization 
vector, or IV.

Implement CBC mode by hand by taking the ECB function you wrote earlier, 
making it encrypt instead of decrypt (verify this by decrypting whatever 
you encrypt to test), and using your XOR function from the previous 
exercise to combine them.

The file here is intelligible (somewhat) when CBC decrypted against 
"YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)

Don't cheat.

Do not use OpenSSL's CBC code to do CBC mode, even to verify your results. 
What's the point of even doing this stuff if you aren't going to learn 
from it?
"""

#######################################
# IMPORTS
#######################################

from hexstr import Hexstr
from binascii import a2b_base64
from Crypto.Cipher import AES

#######################################
# FUNCTIONS
#######################################
def cbc_mode_encrypt(aes_ecb_obj, plain, keylen, iv):
    """Implement CBC mode encryption. plain and iv are byte strings."""
    hexstr_iv = Hexstr(iv)
    hexstr_plain = Hexstr(plain)
    result = ''
    # Converting bytes to hexstr doubles the length of the string..
    start, end = 0, keylen * 2
    for block in range(len(hexstr_plain) // keylen // 2):
        if block == 0:
            cipher = hexstr_iv
            continue
        else:
            xor_result = xor_strings(hexstr_plain[start:end], cipher)
            cipher = aes_ecb_obj.encrypt(xor_result)
            result += bytes_to_hexstr(cipher)
            start, end = end, (end + (keylen * 2))
    return result

def cbc_mode_decrypt(aes_ecb_obj, message, keylen, iv):
    """Implement CBC mode decryption. message and iv are byte strings."""
    start, end = 0, keylen
    prev_cipher = Hexstr(iv)
    result = Hexstr('')
    for block in range(len(message) // keylen):
        cipher = Hexstr(message[start:end])
        decrypted = Hexstr(aes_ecb_obj.decrypt(cipher.bytestr))
        plain = decrypted ^ prev_cipher
        result.update(result.value + plain.value)
        prev_cipher = cipher
        start, end = end, end + keylen
    return result


#######################################
# MAIN
#######################################

with open('10.txt') as infile:
    encrypted = a2b_base64(infile.read())

key = 'YELLOW SUBMARINE'
keylen = len(key)
iv = b'\x00' * keylen
aes_ecb_obj = AES.new(key, AES.MODE_ECB)
cbc_result = cbc_mode_decrypt(aes_ecb_obj, encrypted, keylen, iv)
print(cbc_result.bytestr.decode())
