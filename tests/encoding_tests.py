"""
Tests for encoding part
"""
from unittest import TestCase, main

from common_utils import get_path_to_resource
from src.encoding import encode, _encode_number, _encode_number_into_another_number


class TestingClass(TestCase):
    def test_encoding_one_value(self):
        """
        Test that one integer encoded correctly with different bit_count value
        """
        value = 127
        for i in range(1, 9):
            encoded, _ = _encode_number_into_another_number(value, 0, i, 8 - 1)
            self.assertEqual(encoded, 2 ** (i - 1) - 1)

    def test_overflow(self):
        """
        Test that program run correct when data cannot be encoded
        because of lack of space
        """
        self.assertRaises(SystemExit,
                          encode, get_path_to_resource('in.bmp'), get_path_to_resource('in.bmp'),
                          get_path_to_resource('out file.bmp'))

if __name__ == 'main':
    main()
