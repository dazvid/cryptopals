#!/usr/bin/python3

"""
test_hexstr.py

Unit tests for the class hexstr.
"""

from hexstr import Hexstr, InvalidHexstrError
from binascii import unhexlify
import unittest


class KnownValues(unittest.TestCase):

    valid_hexstrs = ('49276d20', '1234567890abcdef', 'aAbBcCdDeEfF', '0123')
    valid_strs = ('49276d2', '1234abcg', 'AbCdEfGh', '01234', 'Steve')
    invalid_input = (1.5, True, False, None, [1, 2, 3], {'key': 123})
    printable = (b'This should be OK', b'As is this', b'And maybe this?')
    non_printable = (b'\x00', b'\x07', b'This \xff\xf3')

    def test_instantiation_valid_hexstrs(self):
        """Test valid hexstrs used for instantiation"""
        for hs in self.valid_hexstrs:
            newhexstr = Hexstr(hs)
            self.assertEqual(newhexstr.value, hs)

    def test_instantiation_valid_strs(self):
        """Test valid strs used for instantiation"""
        for valid_str in self.valid_strs:
            newhexstr = Hexstr(valid_str)
            self.assertEqual(newhexstr.bytestr.decode('utf-8'), valid_str)

    def test_instantiate_from_bytes(self):
        """Test a valid bytestr used for instantiation"""
        valid_bytestr = b'\x49\x27\x6d\x20'
        valid_hexstr = '49276d20'
        result = Hexstr(valid_bytestr)
        self.assertEqual(valid_hexstr, result.value)

    def test_instantiate_from_int(self):
        """Test a valid int used for instantiation"""
        valid_int = 123
        valid_hexstr = '7b'
        result = Hexstr(valid_int)
        self.assertEqual(valid_hexstr, result.value)

    def test_instantiate_from_negative_int(self):
        """Test an invalid int used for instantiation"""
        invalid_int = -123
        self.assertRaises(InvalidHexstrError, Hexstr, invalid_int)

    def test_instantiation_invalid_types(self):
        """Test for invalid types being passed in to class"""
        for badtype in self.invalid_input:
            with self.subTest(badtype=badtype):
                self.assertRaises(TypeError, Hexstr, badtype)

    def test_to_base64_valid(self):
        """to_base64 should give valid known result with known input"""
        original = Hexstr('49276d20')
        result = original.to_base64()
        self.assertEqual('SSdtIA==', result)

    def test_to_base64_invalid(self):
        """to_base64 should not equal given known bad input"""
        original = Hexstr('49276d20')
        result = original.to_base64()
        self.assertNotEqual('2SdtIA==', result)

    def test_xor(self):
        """xor operator should act like normal bitwise xor on Hexstr objs"""
        hexstr1 = Hexstr('1c0111001f010100061a024b53535009181c')
        hexstr2 = Hexstr('686974207468652062756c6c277320657965')
        expected_result = Hexstr('746865206b696420646f6e277420706c6179')
        result = hexstr1 ^ hexstr2
        self.assertEqual(result.value, expected_result.value)

    def test_xor_wrongtype(self):
        """xor'ing a Hexstr obj with a normal str should fail with TypeError"""
        hexstr1 = Hexstr('1c0111001f010100061a024b53535009181c')
        hexstr2 = '686974207468652062756c6c277320657965'
        self.assertRaises(TypeError, hexstr1.__xor__, hexstr2)

    def test_is_printable(self):
        """Test that each byte in a printable Hexstr is printable"""
        for value in self.printable:
            hs = Hexstr(value)
            self.assertTrue(hs.is_printable())

    def test_is_not_printable(self):
        """Test that each byte in a non-printable Hexstr is printable"""
        for value in self.non_printable:
            hs = Hexstr(value)
            self.assertFalse(hs.is_printable())

if __name__ == '__main__':
    unittest.main()
