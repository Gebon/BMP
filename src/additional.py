"""
Module for additional methods that needn't to encode/decode,
but very useful for theirs implementing
"""
from argparse import ArgumentParser
from math import ceil

from bit_map_file_header import BitMapFileHeader


def create_argument_parser():
    """
    Create command-line arguments parser

    :return: argparse.ArgumentParser object
    """
    parser = ArgumentParser(description='Program to encode '
                            'something to BMP file')
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


class DataLossPossibility(Exception):
    """
    Indicates that data will be lost with such configuration
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Your data will be lost'
        Exception.__init__(self, msg)
        self.msg = msg


class NotEncodedError(Exception):
    """
    Indicates that file is not encoded, i.e. there is no 
    hidden data within BMP file 
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = "This file doesn't encoded"
        Exception.__init__(self, msg)
        self.msg = msg


def read_bytearray_from_file(path: str) -> bytearray:
    """
    Read file in binary format and return it as bytearray
    :param path: path to file
    """
    with open(path, 'rb') as file:
        return bytearray(file.read())


def get_file_header(bmp_data):
    """
    Get file header from BMP file data
    :param bmp_data: bytearray
    :return: BitMapFileHeader instance
    :raise InvalidFileHeader:
    """
    file_header = BitMapFileHeader(bmp_data)
    if file_header.type != 'BM':
        raise InvalidFileHeader()
    return file_header


class InvalidFileHeader(Exception):
    """
    Indicates that this header is not of BMP type 
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Invalid file header'
        Exception.__init__(self, msg)
        self.msg = msg


def check_data_loss_possibility(file_data: bytearray, bmp_data: bytearray, bit_count: int):
    """
    Check that data can be encoded without loss
    :param file_data: file to encoding
    :param bmp_data: container for file data
    :param bit_count: count of bits in each byte
    :raise DataLostPossibility: exception
    """
    if ceil(len(file_data) * 8 / bit_count) > len(bmp_data):
        raise DataLossPossibility()


def try_get_file_header(bmp_data: bytearray) -> BitMapFileHeader:
    """
    Try to get BMP file header. If it's not BMP file, exits with code = 2
    :param bmp_data: potentially bmp file data
    :return: extracted header
    """
    try:
        return get_file_header(bmp_data)
    except InvalidFileHeader:
        print("This file doesn't look like BMP")
        exit(2)


def write_to(path: str, data: bytearray):
    """
    Write bytearray content to file specified by path
    :param path: path to target file
    :param data: data to write
    """
    with open(path, 'wb') as file:
        file.write(data)


def split_bytearray(bytearr: bytearray, offset: int):
    """
    Split bytearray into two parts by offset
    :param bytearr: bytearray to split
    :param offset: offset
    :return: tuple with two parts of bytearray
    """
    return bytearr[:offset], bytearr[offset:]
