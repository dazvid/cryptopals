#!/usr/bin/python3

"""
Detect single-character XOR

One of the 60-character strings in this file (4.txt) has been encrypted by single-character XOR.

Find it.

File contains new line seperated strings like:
    │0e3647e8592d35514a081243582536ed3de6734059001e3f535ce6271032
    │334b041de124f73c18011a50e608097ac308ecee501337ec3e100854201d
etc.

(Your code from #3 should help.)
"""

from binascii import hexlify, unhexlify, b2a_qp
import sys

def xor_strings(xs, ys):
    """
    Take two strings, xs - an encrypted hex string, ys - a single byte XOR key (also a hex string)
    assumes the strings are passed as utf-8, and will return a hex string also as utf-8
    """
    # I'm guessing this could be a one liner, but with all of the conversions
    # it's much more readable to split it out like this..
    xor_byte_string = b''
    for x, y in zip(unhexlify(xs), unhexlify(ys)):
        xor_byte_string += int(x ^ y).to_bytes(1, sys.byteorder)
    return hexlify(xor_byte_string).decode('utf-8')

def is_english_word(word, wordset):
    return word.lower() in wordset

def is_english_phrase(phrase, wordset):
    "If string has more than 3 English words, probably decrypted properly"
    english_word_count = 0
    threshhold = 3
    for word in phrase.lower().split(' '):
        if(is_english_word(word, wordset)):
            english_word_count += 1
    return english_word_count >= threshhold

# Create a set of English words for later scoring
with open("./english-words/words.txt") as word_file:
    english_words = set(word.strip().lower() for word in word_file)

# Create a set of encoded hex strings
with open("4.txt") as encoded_string_file:
    encoded_hexstr_set = set(hexstr.strip() for hexstr in encoded_string_file)

# Brute force each encoded hexstr 
for hexstr in encoded_hexstr_set:
    key_len = int(len(hexstr)/2)

    # Brute force every byte 0 -> 255 (\x00 -> \xFF)
    for key in range(0, 256):
        # generate a hex string 'key' the same length as the encoded string
        xor_key = hexlify(chr(key).encode('latin-1') * key_len).decode('latin-1')
        xor_result = xor_strings(hexstr, xor_key)
        try:
            unicode_string = unhexlify(xor_result).decode('ascii')
        except UnicodeDecodeError:
            pass
        else:
            if is_english_phrase(unicode_string, english_words):
                print('For hexstr: {}'.format(hexstr))
                print('with key: {}'.format(xor_key))
                print(unicode_string)
