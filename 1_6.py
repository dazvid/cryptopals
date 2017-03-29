#!/usr/bin/python3

"""
1_6.py

Break repeating-key XOR
It is officially on, now.

This challenge isn't conceptually hard, but it involves actual error-prone coding. The other challenges in this set are there to bring you up to speed. This one is there to qualify you. If you can do this one, you're probably just fine up to Set 6.

There's a file here. It's been base64'd after being encrypted with repeating-key XOR.

Decrypt it.

Here's how:

- Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
- Write a function to compute the edit distance/Hamming distance between two strings. The Hamming distance is just the number of differing bits. The distance between:

    this is a test
        and
    wokka wokka!!!

  is 37. Make sure your code agrees before you proceed.

- For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes, and find the edit distance between them. Normalize this result by dividing by KEYSIZE.

- The KEYSIZE with the smallest normalized edit distance is probably the key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.

- Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.

- Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.

- Solve each block as if it was single-character XOR. You already have code to do this.

- For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.

- This code is going to turn out to be surprisingly useful later on. Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing. But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important.

- No, that's not a mistake.

- We get more tech support questions for this challenge than any of the other ones. We promise, there aren't any blatant errors in this text. In particular: the "wokka wokka!!!" edit distance really is 37.
"""

from binascii import hexlify, unhexlify, a2b_base64
from itertools import cycle, zip_longest
import freqy
import string
import sys

def bin_string(s):
    "Take a string and make it a binary representation"
    return ''.join('{0:08b}'.format(ord(c)) for c in s)

def hexstr(s):
    "Pass a normal utf-8 string, and get a hexstr back"
    return hexlify(s.encode('utf-8')).decode('utf-8')

def bytes_to_hexstr(bs):
    "Pass a byte string and return a hexstr back"
    return hexlify(bs).decode('utf-8')

def hexstr_to_str(hexstr):
    "Take a hexstr and convert it to printable utf-8"
    return unhexlify(hexstr).decode('utf-8')

def repeating_xor(message, key):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, cycle(key)))

def hamming_distance(s1, s2):
    "Calculate the hamming distance between two strings"
    return sum(c1 != c2 for c1, c2 in zip(bin_string(s1), bin_string(s2)))

def xor_strings(xs, ys):
    """
    Take two strings, xs - an encrypted hex string and 
    ys - a single byte XOR key (also a hex string)
    assumes the strings are passed as utf-8, and will return a hex string also as utf-8
    """
    xor_byte_string = b''
    for x, y in zip(unhexlify(xs), unhexlify(ys)):
        xor_byte_string += int(x ^ y).to_bytes(1, sys.byteorder)
    return hexlify(xor_byte_string).decode('utf-8')


with open('6.txt') as infile:
    encrypted = a2b_base64(infile.read())

# Guess keysize by calculating hamming distance between groups of bytes
best_guess_key = 0 
lowest_distance = 100
for keysize in range(2,41):
    # take keysize amount of bytes and compare it to the second lot of 
    # keysize worth bytes
    chunks = []
    num_chunks = int(len(encrypted)/2)
    start, end = 0, keysize
    for _ in range(num_chunks):
        chunks.append(encrypted[start:end])
        start, end = end, end + keysize

    # find the hamming distance between them
    chunked_hexstr = [bytes_to_hexstr(s) for s in chunks]
    distances = []
    for i in range(num_chunks - 1):
        distances.append(hamming_distance(chunked_hexstr[i], chunked_hexstr[i+1]))

    # normalise by dividing by keysize
    normalised = [distance / keysize for distance in distances]
    result = sum(normalised) / len(normalised)
    if result < lowest_distance:
        lowest_distance = result
        best_guess_key = keysize

print('Best key is {} with a hamming distance of {}'.format(best_guess_key, 
                                                            lowest_distance))
keysize = best_guess_key 

# Break cipher text into blocks of keysize
chunked_cipher = (encrypted[i:i + keysize] for i in range(0, len(encrypted), keysize))

# Transpose each first byte to a new string, second byte to a second 
# string.. etc.
transposed = (bytes(t) for t in zip_longest(*chunked_cipher, fillvalue=0))

# Hold the highest scores and associated keys for each block
highest_score = 0
blocks_best_keys = [dict() for _ in range(keysize)] 

# Determine highest English char frequency for each block
for block_number, message in enumerate(transposed):
    print('\n----------------- block {} ------------------\n'.format(block_number))
    hexstr = bytes_to_hexstr(message)
    # For every byte \x00 -> \xFF
    for char in range(0, 256):
        key_len = int(len(hexstr) / 2)
        bytes_key = (chr(char) * key_len).encode('latin-1')
        key = bytes_to_hexstr(bytes_key)
        xor_result = xor_strings(hexstr, key)
        try:
            unicode_string = unhexlify(xor_result).decode('latin-1')
        except UnicodeDecodeError:
            pass
        else:
            score = freqy.english_freq_match_score(unicode_string)
            if score >= highest_score:
                if score not in blocks_best_keys[block_number]:
                    blocks_best_keys[block_number][score] = [key[:2]]
                else:
                    blocks_best_keys[block_number][score].append(key[:2])
                highest_score = score

    print('Score {}: for keys:'.format(highest_score))
    for key in blocks_best_keys[block_number][highest_score]:
        print(key)

    # Reset score for next block
    highest_score = 0 
