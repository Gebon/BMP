import unittest
from common_utils import get_path_to_resource
from src.encoding import encode
from src.decoding import decode
from src.additional import read_bytearray_from_file


class FunctionalTestCase(unittest.TestCase):
    def test_functional(self):
        """
        Functional test for program

        """
        for i in range(1, 9):
            encode(get_path_to_resource('in.bmp'), get_path_to_resource('file.jpg'),
                   get_path_to_resource('out file.bmp'), i)
            decode(get_path_to_resource('out file.bmp'), get_path_to_resource('decoded_file.jpg'))
            self.assertEqual(
                read_bytearray_from_file(get_path_to_resource('decoded_file.jpg')),
                read_bytearray_from_file(get_path_to_resource('file.jpg'))
            )


if __name__ == '__main__':
    unittest.main()
