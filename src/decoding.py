"""
Main module for decoding
"""
__author__ = 'Галлям'

from math import ceil

from src.additional import read_bytearray_from_file, try_get_file_header,\
    split_bytearray, write_to, NotEncodedError


def check_encoded(bmp_data, msg):
    """
    Check's that file was encoded by encode() function
    :param bmp_data: bytearray
    :param msg: message that must be encoded in data
    :raise NotEncodedError: say that file not encoded
    """
    decoded_msg = _decode(bmp_data, 1, len(msg))
    if msg != decoded_msg:
        raise NotEncodedError()


def _decode_specified_bits(data, bit_count, bits=8, start_index=0):
    """
    Decode specified bits and return result
    :param data: bytearray
    :param bit_count: integer
    :param bits: integer
    :param start_index: integer
    :return: integer value
    """
    counter = 0
    result = 0
    is_end = False
    bits_left = bits
    shift = 0
    for index in range(start_index, len(data)):
        delta = 0
        if bits_left < bit_count:
            delta = bit_count - bits_left
        result <<= shift - delta
        shift = 0
        for i in range(bit_count - 1, -1, -1):
            if data[index] >> i & 1:
                result |= 1 << i - delta
            else:
                result &= ~(1 << i - delta)
            counter += 1
            if counter == bits:
                is_end = True
                break
            shift += 1
        bits_left -= bit_count
        if is_end:
            break
    return result


def _decode(data, bit_count, data_length_in_bytes=None):
    """
    Internal decode method
    :param data: bytearray
    :param bit_count: integer
    :param data_length_in_bytes: integer
    :return: decode data as bytearray
    """
    result = bytearray()
    if data_length_in_bytes is None:
        data_length = len(data)
    else:
        data_length = data_length_in_bytes
    for i in range(0, int(data_length)):
        result.append(_decode_specified_bits(data, bit_count, 8,
                                             ceil(8 / bit_count) * i))
    return result


def decode(file_to_decode_path, out_file_path):
    """
    Decode file and write decoded data to out_file_path
    :param file_to_decode_path: obviously
    :param out_file_path: obviously
    """
    bmp_data = read_bytearray_from_file(file_to_decode_path)

    file_header = try_get_file_header(bmp_data)

    bmp_data = split_bytearray(bmp_data, file_header.off_bits)[1]

    msg = b'encoded'
    try:
        check_encoded(bmp_data, msg)
    except NotEncodedError:
        print("This file doesn't encoded. I can do nothing. Sorry...")
        exit(3)

    bmp_data = bmp_data[len(msg) * 8:]

    bits_for_file_length = 32
    file_length_data, bmp_data = split_bytearray(bmp_data, bits_for_file_length)

    file_length = _decode_specified_bits(file_length_data, 1,
                                         bits_for_file_length)

    bit_count_data, bmp_data = split_bytearray(bmp_data, 3)

    bit_count = _decode_specified_bits(bit_count_data, 1, 3) + 1

    file_data = _decode(bmp_data, bit_count, file_length)

    write_to(out_file_path, file_data)

