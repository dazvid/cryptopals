#!/usr/bin/python3

"""
1_5.py

Implement repeating-key XOR

Here is the opening stanza of an important work of the English language:

    Burning 'em, if you ain't quick and nimble
    I go crazy when I hear a cymbal

    Encrypt it, under the key "ICE", using repeating-key XOR.

    In repeating-key XOR, you'll sequentially apply each byte of the key; the first byte of plaintext will be XOR'd against I, the next C, the next E, then I again for the 4th byte, and so on.

    It should come out to:

        0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
        a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

        Encrypt a bunch of stuff using your repeating-key XOR function. Encrypt your mail. Encrypt your password file. Your .sig file. Get a feel for it. I promise, we aren't wasting your time with this.

"""

from binascii import hexlify, unhexlify
from itertools import cycle

def hexstr(s):
    "Pass a normal utf-8 string, and get a hexstr back"
    return hexlify(s.encode('utf-8')).decode('utf-8')

def hexstr_to_str(hexstr):
    "Take a hexstr and convert it to printable utf-8"
    return unhexlify(hexstr).decode('utf-8')

def repeating_xor(message, key):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, cycle(key)))

stanza = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
key = 'ICE'

print('Original:\n{}'.format(stanza))
print('Encrypting with key: {}'.format(key))

encrypted = repeating_xor(stanza, key)
print('Encrypted:\n{}'.format(encrypted))

print(type(encrypted))
decrypted = repeating_xor(encrypted, key)
print('Decrypted:\n{}'.format(decrypted))
