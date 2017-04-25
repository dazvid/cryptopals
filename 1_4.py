#!/usr/bin/python3

"""
Detect single-character XOR

One of the 60-character strings in this file (4.txt) has been encrypted 
by single-character XOR.

Find it.

File contains new line seperated strings like:
    │0e3647e8592d35514a081243582536ed3de6734059001e3f535ce6271032
    │334b041de124f73c18011a50e608097ac308ecee501337ec3e100854201d
etc.

(Your code from #3 should help.)
"""

##########################
# IMPORTS
##########################

from hexstr import Hexstr, single_byte_xor
from isenglish import IsEnglish

##########################
# MAIN
##########################

# Instantiating the IsEnglish() class will read a dictionary from a file
# and generate a wordset
english_tester = IsEnglish()

# Create a set of encoded hex strings
with open("4.txt") as encoded_string_file:
    encoded_hexstr_set = set(Hexstr(hs.strip()) for hs in encoded_string_file)

# Brute force each encoded hexstr 
for hexstr in encoded_hexstr_set:
    for result, key in single_byte_xor(hexstr):
        if result.is_printable():
            decoded = result.bytestr.decode()
            if english_tester.is_english_phrase(decoded):
                print('For hexstr: {}'.format(hexstr))
                print('with key: {}'.format(key.value))
                print(decoded)
                break
