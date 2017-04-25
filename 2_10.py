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

def cbc_mode_encrypt(aes_ecb_obj, message, keylen, iv):
    """Implement CBC mode encryption. Message and iv are byte strings."""
    start, end = 0, keylen
    prev_cipher = Hexstr(iv)
    result = Hexstr('')
    for block in range(len(message) // keylen):
        plain = Hexstr(message[start:end])
        xor_result = plain ^ prev_cipher
        encrypted = Hexstr(aes_ecb_obj.encrypt(xor_result.bytestr))
        result.update(result.value + encrypted.value)
        prev_cipher = encrypted
        start, end = end, end + keylen
    return result

def cbc_mode_decrypt(aes_ecb_obj, message, keylen, iv):
    """Implement CBC mode decryption. Message and iv are byte strings."""
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

if __name__ == '__main__':

    with open('10.txt') as infile:
        encrypted = a2b_base64(infile.read())

    key = 'YELLOW SUBMARINE'
    keylen = len(key)
    iv = b'\x00' * keylen
    aes_ecb_obj = AES.new(key, AES.MODE_ECB)

    print('Decrypting... {} bytes'.format(len(encrypted)))
    print('--------------------------------')
    result = cbc_mode_decrypt(aes_ecb_obj, encrypted, keylen, iv)
    decrypted = result.bytestr.decode('utf-8')
    print(decrypted)

    print('Custom encrypting... {} bytes'.format(len(decrypted)))
    print('--------------------------------')
    encrypted = cbc_mode_encrypt(aes_ecb_obj, decrypted, keylen, iv)
    print(encrypted.value)

    print('Decrypting... {} bytes'.format(len(encrypted.bytestr)))
    print('--------------------------------')
    decrypted = cbc_mode_decrypt(aes_ecb_obj, encrypted.bytestr, keylen, iv)
    print(decrypted.bytestr.decode('utf-8'))
