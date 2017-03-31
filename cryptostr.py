#!/usr/bin/python3

"""
cryptostr.py

Contains a few conversions used in the cryptopals challenges.

Examples:

- bin_string:
    "test" -> "01110100011001010111001101110100"

- int_to_hexstr
    1 -> '01', 255 -> 'ff', etc.

- hexstr
    "test" -> "74657374"

- bytes_to_hexstr:
    b'' -> ''

- hexstr_to_str:
    "74657374" -> "test"  
    
- hamming_distance:
    s1 = "this is a test" & s2 = "wokka wokka!!!" == 37

- xor_strings:
    takes two strings, and xors them together
    hexstr1 = '1c0111001f010100061a024b53535009181c'
    hexstr2 = '686974207468652062756c6c277320657965'
    result will be:
    '746865206b696420646f6e277420706c6179'

"""

from binascii import hexlify, unhexlify
import sys

def int_to_hexstr(value):
    "Convert an int value into a short hexstr"
    return '{0:02x}'.format(value)

def hexstr(s):
    "Pass a normal utf-8 string, and get a hexstr back"
    return hexlify(s.encode('utf-8')).decode('utf-8')

def bytes_to_hexstr(bs):
    "Pass a byte string and return a hexstr back"
    return hexlify(bs).decode('utf-8')

def hexstr_to_str(hexstr):
    "Take a hexstr and convert it to printable utf-8"
    try: 
        s = unhexlify(hexstr).decode('utf-8')
    except UnicodeDecodeError:
        return None
    else:
        return s

def bin_string(s):
    "Take a string and make it a binary representation"
    return ''.join('{0:08b}'.format(ord(c)) for c in s)

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
