__author__ = 'Галлям'

from unittest import TestCase, main

from encoding import encode, _encode_to_byte
from decoding import decode, _decode_specified_bits
from additional import read_bytearray_from_file, DataLostPossibility


class TestingClass(TestCase):
    def setUp(self):
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
        for i in range(1, 9):
            data = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')
            _encode_to_byte(self.value, i, 8, data)
            TestCase.assertEqual(self, data, self.res_data[i])

    def test_decoding_one_value(self):
        for i in range(1, 9):
            self.assertEqual(_decode_specified_bits(self.res_data[i], i),
                             self.value)

    def test_functional(self):
        for i in range(2, 9):
            encode(r'test_res\in.bmp', r'test_res\file.bmp',
                   r'test_res\out file.bmp', i)
            decode(r'test_res\out file.bmp', r'test_res\decode_file.bmp')
            self.assertEqual(
                read_bytearray_from_file(r'test_res\decode_file.bmp'),
                read_bytearray_from_file(r'test_res\in.bmp')
            )

    def test_overflow(self):
        self.assertRaises(DataLostPossibility, encode,
                          r'test_res\in.bmp', r'test_res\file.bmp',
                          r'test_res\out file.bmp')


if __name__ == 'main':
    main()