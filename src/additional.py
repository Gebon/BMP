"""
Module for additional methods that needn't to encode/decode,
but very useful for theirs implementing
"""
__author__ = 'Галлям'

from struct import unpack_from
from argparse import ArgumentParser
from math import ceil

from src.bit_map_file_header import BitMapFileHeader, FILE_HEADER_FMT


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


class WrongArgument(BaseException):
    """
    Exception class
    """
    def __init__(self, msg):
        BaseException.__init__(self)
        self.msg = msg


class DataLostPossibility(Exception):
    """
    Exception class
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Your data will be lost'
        Exception.__init__(self, msg)
        self.msg = msg


class NotEncodedError(Exception):
    """
    Exception class
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = "This file doesn't encoded"
        Exception.__init__(self, msg)
        self.msg = msg


def read_bytearray_from_file(path):
    """
    Read bytes from file, convert it to bytearray and return
    :param path: path to file
    :return: bytearray
    """
    with open(path, 'rb') as file:
        return bytearray(file.read())


def read_readme():
    """
    Print to the console README.md file

    """
    with open('README.md', encoding='utf8') as readme:
        for line in readme:
            print(line)


def get_file_header(bmp_data):
    """
    Get file header from BMP file data
    :param bmp_data: bytearray
    :return: bit_map_file_header instance :raise InvalidFileHeader:
    """
    file_header = BitMapFileHeader(unpack_from(FILE_HEADER_FMT, bmp_data))
    if file_header.type != 'BM':
        raise InvalidFileHeader()
    return file_header


class InvalidFileHeader(Exception):
    """
    Exception class
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Invalid file header'
        Exception.__init__(self, msg)
        self.msg = msg


def check_data_lost_possibility(file_data, bmp_data, bit_count):
    """
    Check that data can be encoded without loss
    :param file_data: file to encoding
    :param bmp_data: container for file data
    :param bit_count: count of bits in each byte
    :raise DataLostPossibility: exception
    """
    if ceil(len(file_data) * 8 / bit_count) > len(bmp_data):
        raise DataLostPossibility()


def try_get_file_header(bmp_data):
    """
    Try to get BMP file header. If it can't be done, raise an exception
    :param bmp_data: bytearray
    :return: bit_map_file_header instance
    """
    try:
        return get_file_header(bmp_data)
    except InvalidFileHeader:
        print("This file doesn't look like BMP")
        exit(2)


def write_to(path, data):
    """
    Write bytearray content to file specified by path
    :param path: path to target file
    :param data: data to write
    """
    with open(path, 'wb') as file:
        file.write(data)


def split_bytearray(bytearr, offset):
    """
    Split bytearr by offset
    :param bytearr: bytearr to split
    :param offset: offset
    :return: tuple with to part of bytearr
    """
    return bytearr[:offset], bytearr[offset:]
