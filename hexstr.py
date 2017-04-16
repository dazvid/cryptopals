#!/usr/bin/python3

"""
hexstr.py

A class representation of a hex string. 

Contains functions to encode, decode, xor & manipulate hexstr's
suited for the cryptopals.com challenges.
"""

from binascii import hexlify, unhexlify, b2a_base64 
import re


class InvalidHexstr(ValueError):
    """Raise when hexstr is incorrect length or contains illegal chars"""


class Hexstr():
    """Hexstring class with conversion and crypto operations"""

    valid_hex_chars = re.compile(r'[0-9a-f]', re.IGNORECASE)
    invalid_type_message = 'Hexstr class must be initialized from str, int \
                            or bytes object.'
    invalid_hexstr_message = 'Invalid hexstr -- check length and characters'

    def __init__(self, value=None):
        """Initialize a Hexstr object from str, int or bytes"""
        if isinstance(value, str): 
            if self.validate_hexstr(value):
                self.value = value
                self.bytestr = unhexlify(value)
            else:
                raise InvalidHexstr(self.invalid_hexstr_message )
        elif isinstance(value, bool):
            raise TypeError(self.invalid_type_message)
        elif isinstance(value, bytes):
            self.value = hexlify(value).decode('utf-8')
            self.bytestr = value
        elif isinstance(value, int):
            self.value = '{0:02x}'.format(value)
            self.bytestr = unhexlify(self.value)
        else:
            raise TypeError(self.invalid_type_message)

    def __repr__(self):
        """Print out the hexstr value as a utf-8 string by default"""
        return self.value

    def validate_hexstr(self, hs):
        """Validate the characters and length of a hexstr"""
        if len(hs) % 2 != 0: 
            return False

        allowed = re.compile(r'[0-9a-f]', re.IGNORECASE)
        return all(allowed.match(x) for x in hs)

    def to_base64(self):
        """Return a utf-8 encoded base64 representation of the hexstr"""
        return b2a_base64(self.bytestr).decode('utf-8').strip()

    def __xor__(self, other):
        """xor two hexstrings together, return a new Hexstr obj"""
        if not isinstance(other, Hexstr): 
            raise TypeError("Can't xor non Hexstr objects together")

        return Hexstr(''.join(hex(x ^ y)[2:] for x, y in 
                      zip(self.bytestr, other.bytestr)))


if __name__ == '__main__':
    pass
