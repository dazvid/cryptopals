#!/usr/bin/python3

"""
1_6.py

Break repeating-key XOR
It is officially on, now.

This challenge isn't conceptually hard, but it involves actual 
error-prone coding. The other challenges in this set are there 
to bring you up to speed. This one is there to qualify you. If 
you can do this one, you're probably just fine up to Set 6.

There's a file here. It's been base64'd after being encrypted with 
repeating-key XOR.

Decrypt it.

Here's how:

- Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
- Write a function to compute the edit distance/Hamming distance between 
two strings. The Hamming distance is just the number of differing bits. 
The distance between:

    this is a test
        and
    wokka wokka!!!

is 37. Make sure your code agrees before you proceed.

- For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second 
KEYSIZE worth of bytes, and find the edit distance between them. Normalize 
this result by dividing by KEYSIZE.

- The KEYSIZE with the smallest normalized edit distance is probably the 
key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or 
take 4 KEYSIZE blocks instead of 2 and average the distances.

- Now that you probably know the KEYSIZE: break the ciphertext into blocks 
of KEYSIZE length.

- Now transpose the blocks: make a block that is the first byte of every 
block, and a block that is the second byte of every block, and so on.

- Solve each block as if it was single-character XOR. You already have 
code to do this.

- For each block, the single-byte XOR key that produces the best looking 
histogram is the repeating-key XOR key byte for that block. Put them 
together and you have the key.

- This code is going to turn out to be surprisingly useful later on. 
Breaking repeating-key XOR ("Vigenere") statistically is obviously an 
academic exercise, a "Crypto 101" thing. But more people "know how" to 
break it than can actually break it, and a similar technique breaks 
something much more important.

- No, that's not a mistake.

- We get more tech support questions for this challenge than any of the 
other ones. We promise, there aren't any blatant errors in this text. 
In particular: the "wokka wokka!!!" edit distance really is 37.
"""

#######################################
# IMPORTS
#######################################

from cryptostr import hamming_distance, repeating_xor
from binascii import a2b_base64
from itertools import zip_longest
import sys
import string

#######################################
# DEFINES
#######################################

NUM_MOST_FREQ_LETTERS = 5
NUM_CHUNKS = 10
MIN_KEYSIZE = 2
MAX_KEYSIZE = 41

#######################################
# MAIN
#######################################

with open('6.txt') as infile:
    encrypted = a2b_base64(infile.read())

# Guess keysize by calculating hamming distance between groups of bytes
best_guess_key = 0 
lowest_distances = {}
for keysize in range(MIN_KEYSIZE, MAX_KEYSIZE):
    chunks = []
    start, end = 0, keysize
    for _ in range(NUM_CHUNKS):
        chunks.append(encrypted[start:end])
        start, end = end, end + keysize

    # find the hamming distance between them
    chunked_hexstr = [bytes_to_hexstr(s) for s in chunks]
    distances = []
    for i in range(NUM_CHUNKS - 1):
        distances.append(hamming_distance(chunked_hexstr[i], 
                                          chunked_hexstr[i+1]))

    # normalise by dividing by keysize
    normalised = [distance / keysize for distance in distances]
    result = sum(normalised) / len(normalised)
    lowest_distances[keysize] = result

sorted_distances = list(lowest_distances.items())
sorted_distances.sort(key=lambda index: index[1])
sorted_distances = sorted_distances[:NUM_MOST_FREQ_LETTERS] 
print('Keys with the lowest 5 hamming distances:')
for key, freq in sorted_distances:
    print('The key {} has a hamming distance of {}'.format(key, freq))

keysize = int(sorted_distances[0][0])
print('Attempting keysize of: {}'.format(keysize))

# Break cipher text into blocks of keysize
chunked_cipher = (encrypted[i:i + keysize] for i in range(0, len(encrypted), 
                                                          keysize))

# Transpose each first byte to a new string, second byte to a second 
# string.. etc.
transposed = (bytes(t) for t in zip_longest(*chunked_cipher, fillvalue=0))

# Hold the highest scores and associated keys for each block
highest_score = 0
blocks_best_keys = [dict() for _ in range(keysize)] 
blocks_highest_score = []

# Determine highest English char frequency for each block
for block, message in enumerate(transposed):
    blocks_highest_score.append(0)
    hexstr = bytes_to_hexstr(message)
    # Brute force for single byte key
    for key in range(0, 256):
        _, score = score_xor(hexstr, key)
        if score and score >= highest_score:
            short_key = int_to_hexstr(key)
            if score not in blocks_best_keys[block]:
                blocks_best_keys[block][score] = [short_key]
            else:
                blocks_best_keys[block][score].append(short_key)
            highest_score = score
            blocks_highest_score[block] = highest_score
    # Reset score for next block
    highest_score = 0 

# Now we have the highest scores and probable keys... Run through again to 
# determine which of the keys have the best results
# Redo the generators:
chunked_cipher = (encrypted[i:i + keysize] for i in range(0, len(encrypted), 
                                                          keysize))
transposed = (bytes(t) for t in zip_longest(*chunked_cipher, fillvalue=0))
# Print out most likely keys, with some broken out text for manual analysis
finalkey = ''
highest_char_count = 0
for block, message in enumerate(transposed):
    print('------------------- {} -------------------'.format(block))
    print('Possible keys:')
    score = blocks_highest_score[block]
    for key in blocks_best_keys[block][score]:
        printable_key = chr(int(key, 16))
        if printable_key in string.ascii_letters or string.punctuation \
                                                 or string.whitespace:
            result, _ = score_xor(bytes_to_hexstr(message), ord(printable_key))
            filtered_result = ''.join(c for c in result 
                                      if c in string.ascii_lowercase)
            if len(filtered_result) > highest_char_count:
                highest_char_count = len(filtered_result)
                best_key = printable_key
            print('({}) {}: {}'.format(score, printable_key, filtered_result))
    finalkey += best_key
    highest_char_count = 0

print('==========================================')
print('Likely key: {}'.format(finalkey))
print('Attempting to decrypt...')
print('==========================================')
message = encrypted.decode('utf-8')
print(repeating_xor(message, finalkey))
