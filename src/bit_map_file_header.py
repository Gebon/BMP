"""
This module contains only one class
"""

__author__ = 'Галлям'

FILE_HEADER_FMT = '<2sIHHI'


class BitMapFileHeader:
    """
    Class that represent BitMapFileHeader structure
    """
    def __init__(self, info):
        self._type = info[0].decode()
        self.size = info[1]
        self._reserved1 = info[2]
        self._reserved2 = info[3]
        self._off_bits = info[4]

    def __str__(self):
        return 'File type: {0}\r\n' \
               'File size: {1} bytes\r\n' \
               'Off bits: {2}'.format(self.type, self.size, self.off_bits)

    @property
    def off_bits(self):
        """
        Getter for _off_bits field

        :return: integer
        """
        return self._off_bits

    @property
    def type(self):
        """
        Getter for _type field

        :return: Must be "BM". Else means that this file don't BMP file
        """
        return self._type
