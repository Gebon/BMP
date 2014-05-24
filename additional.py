__author__ = 'Галлям'

from struct import unpack_from
from argparse import ArgumentParser
from math import ceil

from bit_map_file_header import BitMapFileHeader, FILE_HEADER_FMT


def create_argument_parser():
    parser = ArgumentParser(description='Program to encode'
                                        ' something to BMP file')
    parser.add_argument('-e', dest='encode', nargs=3,
                        metavar=('<path to bmp file>',
                                 '<path to encoding file>',
                                 '<path to output>'),
                        help='"merger" (encode) smth file and bmp file')
    parser.add_argument('-d', dest='decode', nargs=2,
                        metavar=('<file to decode path>', '<path to output>'),
                        help='decode information from bmp file')
    parser.add_argument('bit_count', nargs="?",
                        help='count of bits in each byte',
                        type=int,
                        default=1)
    parser.add_argument('-i', '--identify', nargs=2,
                        metavar=('<path to file to identify>',
                                 '<output file path>'),
                        help='identify whether or not smth information encoded '
                             'to bmp file')
    return parser


class WrongArgument(BaseException):
    def __init__(self, msg):
        self.msg = msg


class DataLostPossibility(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Your data will be lost'
        self.msg = msg


class NotEncodedError(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = "This file doesn't encoded"
        self.msg = msg


def read_bytearray_from_file(path):
    with open(path, 'rb') as file:
        return bytearray(file.read())


def read_readme():
    with open('README.md', 'rt', encoding='utf8') as readme:
        for line in readme:
            print(line)


def get_file_header(bmp_data):
    file_header = BitMapFileHeader(unpack_from(FILE_HEADER_FMT, bmp_data))
    if file_header.type != 'BM':
        raise InvalidFileHeader()
    return file_header


class InvalidFileHeader(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Invalid file header'
        self.msg = msg


def check_data_lost_possibility(file_data, bmp_data, bit_count):
    if ceil(len(file_data) * 8 / bit_count) > len(bmp_data):
        raise DataLostPossibility()


def try_get_file_header(bmp_data):
    try:
        return get_file_header(bmp_data)
    except InvalidFileHeader:
        print("This file doesn't look like BMP")
        exit(2)


def write_to(path, data):
    with open(path, 'wb') as file:
        file.write(data)


def split_bytearray(bytearr, offset):
    return bytearr[:offset], bytearr[offset:]