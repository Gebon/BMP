__author__ = 'Галлям'

FILE_HEADER_FMT = '<2sIHHI'


class BitMapFileHeader:
    def __init__(self, info):
        self.type = info[0].decode()
        self.size = info[1]
        self._reserved1 = info[2]
        self._reserved2 = info[3]
        self.off_bits = info[4]

    def __str__(self):
        return 'File type: {0}\r\n' \
               'File size: {1} bytes\r\n' \
               'Off bits: {2}'.format(self.type, self.size, self.off_bits)
