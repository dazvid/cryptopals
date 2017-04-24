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

from freqy import chi_squared
from hexstr import Hexstr

def bruteforce_xor(message):
    """Brute force single byte xor decrypt.
    
    Message is passed as a Hexstr object. Return a list of results,
    and their accompanying Chi Squared Statistic value.
    """
    results = []
    for i in range(256):
        # Generate an approrpiate Hexstr key
        xorkey = Hexstr(i)
        xorkey.update(xorkey.value * (len(message.value) // 2))
        result = message ^ xorkey
        if result.is_printable():
            score = chi_squared(result.value)
            results.append((result, score, i))
    return results


if __name__ == "__main__":

    message = \
    '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

    hs = Hexstr(message)
    all_guesses = bruteforce_xor(hs)
    # grab the top 5 results
    best_guesses = sorted(all_guesses, key=lambda score: score[1])[:5]
    for guess in best_guesses:
        str_repr = guess[0].bytestr.decode() 
        print('(0x{:x}) {:.2f}: {}'.format(guess[2], guess[1], str_repr))
