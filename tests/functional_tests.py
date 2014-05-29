__author__ = 'Галлям'

import unittest
from src.encoding import encode
from src.decoding import decode
from src.additional import read_bytearray_from_file

class FunctionalTestCase(unittest.TestCase):
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



if __name__ == '__main__':
    unittest.main()
