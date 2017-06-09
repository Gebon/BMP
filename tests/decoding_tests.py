"""
Tests for encoding part
"""
from unittest import TestCase, main

from common_utils import get_path_to_resource
from src.decoding import decode, _decode_specified_bits


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

    def test_decoding_one_value(self):
        """
        Test that decoding one value return correct answer

        """
        for i in range(1, 9):
            self.assertEqual(_decode_specified_bits(self.res_data[i], i),
                             self.value)

    def test_not_bmp_to_decode(self):
        """
        Test that program correctly exit if we try to encode wrong file
        """
        self.assertRaises(SystemExit, decode,
                          get_path_to_resource('in.bmp'), get_path_to_resource('out file.bmp'))

if __name__ == 'main':
    main()
