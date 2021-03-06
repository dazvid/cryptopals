#!/usr/bin/python3

"""
Single-byte XOR cipher

The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt 
the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. 
Character frequency is a good metric. Evaluate each output and choose 
the one with the best score. 
"""

from binascii import hexlify, unhexlify
import sys

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

def get_wordset():
    "Attempt to open the default english wordlist I downloaded from some random git"
    # Create a set of English words for later scoring
    with open("./english-words/words.txt") as word_file:
        english_words = set(word.strip().lower() for word in word_file)
    return english_words

def xor_strings(xs, ys):
    """
    Take two strings, xs - an encrypted hex string, ys - a single byte 
    XOR key (also a hex string) assumes the strings are passed as utf-8, 
    and will return a hex string also as utf-8
    """
    # I'm guessing this could be a one liner, but with all of the conversions
    # it's much more readable to split it out like this..
    xor_byte_string = b''
    for x, y in zip(unhexlify(xs), unhexlify(ys)):
        xor_byte_string += int(x ^ y).to_bytes(1, sys.byteorder)
    return hexlify(xor_byte_string).decode('utf-8')

def break_single_byte_xor(hexstr):
    english_words = get_wordset()
    buf_len = int(len(hexstr)/2)

    # Brute force every byte 0 -> 255 (\x00 -> \xFF)
    for key in range(0, 256):
        # generate a hex string 'key' the same length as the encoded string
        xor_key = hexlify(chr(key).encode('latin-1') * buf_len).decode('latin-1')
        xor_result = xor_strings(hexstr, xor_key)
        try:
            unicode_string = unhexlify(xor_result).decode('utf-8')
        except UnicodeDecodeError:
            pass
        else:
            if is_english_phrase(unicode_string, english_words):
                print('For key: {}'.format(xor_key))
                print(unicode_string)

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        break_single_byte_xor(sys.argv[1])
    else:
        print('Usage: {} <hex_string>'.format(sys.argv[0]))
