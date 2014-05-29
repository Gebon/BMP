"""
Module with tests
"""
__author__ = 'Галлям'

from unittest import TestCase, main

from src.encoding import encode, _encode_to_byte
from src.decoding import decode, _decode_specified_bits
from src.additional import read_bytearray_from_file


class TestingClass(TestCase):
    """
    Class with test functions
    """
    def setUp(self):
        """
        Set's up required data for each test

        """
        self.value = 127
        self.res_data = {1: bytearray(b'\x00\x01\x01\x01\x01\x01\x01\x01'),
                         2: bytearray(b'\x01\x03\x03\x03\x00\x00\x00\x00'),
                         3: bytearray(b'\x03\x07\x06\x00\x00\x00\x00\x00'),
                         4: bytearray(b'\x07\x0f\x00\x00\x00\x00\x00\x00'),
                         5: bytearray(b'\x0f\x1c\x00\x00\x00\x00\x00\x00'),
                         6: bytearray(b'\x1f\x30\x00\x00\x00\x00\x00\x00'),
                         7: bytearray(b'\x3f\x40\x00\x00\x00\x00\x00\x00'),
                         8: bytearray(b'\x7f\x00\x00\x00\x00\x00\x00\x00')}

    def test_encoding_one_value(self):
        """
        Test that one integer encoded correctly with different bit_count value

        """
        for i in range(1, 9):
            data = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')
            _encode_to_byte(self.value, i, 8, data)
            TestCase.assertEqual(self, data, self.res_data[i])

    def test_decoding_one_value(self):
        """
        Test that decoding one value return correct answer

        """
        for i in range(1, 9):
            self.assertEqual(_decode_specified_bits(self.res_data[i], i),
                             self.value)

    def test_functional(self):
        """
        Functional test for program

        """
        for i in range(1, 9):
            encode(r'test_res\in.bmp', r'test_res\file.jpg',
                   r'test_res\out file.bmp', i)
            decode(r'test_res\out file.bmp', r'test_res\decoded_file.jpg')
            self.assertEqual(
                read_bytearray_from_file(r'test_res\decoded_file.jpg'),
                read_bytearray_from_file(r'test_res\file.jpg')
            )

    def test_overflow(self):
        """
        Test that program run correct when data can't be encoded
        because of not enough space
        """
        self.assertRaises(SystemExit,
                          encode, r'test_res\in.bmp', r'test_res\in.bmp',
                          r'test_res\out file.bmp')

    def test_not_bmp_to_decode(self):
        """
        Test that program correctly exit if we try to encode wrong file
        """
        self.assertRaises(SystemExit, decode,
                         r'test_res\in.bmp', r'test_res\out file.bmp')

if __name__ == 'main':
    main()
