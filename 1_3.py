#!/usr/bin/python3

"""
1_3.py

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

from cryptostr import int_to_hexstr, xor_strings, hexstr_to_str
from freqy import english_freq_match_score

def attempt_xor(message, key):
    "Attempt to brute force a single byte xor key"
    # generate a hex string key the same length as the encoded string
    keylen = int(len(message) / 2)
    xorkey = int_to_hexstr(key) * keylen
    result = xor_strings(message, xorkey)
    if result: result = hexstr_to_str(result)
    if result:
        score = english_freq_match_score(result)
        return result, score
    return None, None

def bruteforce_xor(message, threshold):
    "Brute force each byte for a single byte xor decrypt"
    # Brute force every byte 0 -> 255 (\x00 -> \xFF)
    for key in range(0, 256):
        (result, score) = attempt_xor(message, key)
        if score and score >= threshold:
            print('For key: {} ({})'.format(chr(key), hex(key)))
            print(result)

def is_english_word(word, wordset):
    return word.lower() in wordset

def is_english_phrase(phrase, wordset):
    "If string has more than 3 English words, probably decrypted properly"
    english_word_count = 0
    threshold = 3
    for word in phrase.lower().split(' '):
        if(is_english_word(word, wordset)):
            english_word_count += 1
    return english_word_count >= threshold

if __name__ == "__main__":
    # Create a set of English words for later scoring
    with open("./english-words/words.txt") as word_file:
        english_words = set(word.strip().lower() for word in word_file)

    message = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

    threshold = 4
    bruteforce_xor(message, threshold)
