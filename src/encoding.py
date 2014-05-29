"""
Main module for encoding
"""
__author__ = 'Галлям'

from math import ceil

from src.additional import read_bytearray_from_file, write_to, \
    try_get_file_header, split_bytearray, check_data_lost_possibility, \
    DataLostPossibility


def _encode_to_byte(value, bit_count, elem_size, target, counter=0):
    """
    Function that encode one value with size in bits (elem_size) to target
    bytearray with specified bits per byte (bit_count)
    :param value: one integer value target encode
    :param bit_count: count of bits target encode in current byte
    :param elem_size: size of value in bits
    :param target: target bytearray
    :param counter: count of invokes this method
    :return: new counter value
    """
    shift = elem_size - 1
    is_end = False
    for j in range(0, ceil(elem_size / bit_count)):
        for i in range(bit_count - 1, -1, -1):
            if value >> shift & 1:
                target[j + ceil(elem_size / bit_count) * counter] |= 1 << i
            else:
                target[j + ceil(elem_size / bit_count) * counter] &= ~(1 << i)
            shift -= 1
            if shift == -1:
                is_end = True
                break
        if is_end:
            break
    return counter + 1


def _encode(data, target, bit_count, elem_size):
    """
    Function that encode one sequence of elements target another
    :param data: source sequence
    :param target: target sequence
    :param bit_count: bits per byte
    :param elem_size: size in bits of each element in source
    """
    counter = 0
    for value in data:
        counter = _encode_to_byte(value, bit_count, elem_size, target, counter)


def encode(bmp_file_path, file_to_encode_path, out_file_path, bit_count=1):
    """
    Encode something file to BMP file and record result to out_file_path
    :param bmp_file_path: BMP file
    :param file_to_encode_path: File to encode
    :param out_file_path: Obviously
    :param bit_count: bits per byte
    """
    bmp_data = read_bytearray_from_file(bmp_file_path)
    file_data = read_bytearray_from_file(file_to_encode_path)

    file_header = try_get_file_header(bmp_data)

    bits_for_file_length = 32

    header, bmp_data = split_bytearray(bmp_data, file_header.off_bits)

    msg = b'encoded'
    _encode(bytearray(msg), bmp_data, 1, 8)
    encoded_msg, bmp_data = split_bytearray(bmp_data, len(msg)*8)

    file_length = len(file_data)
    _encode((file_length,), bmp_data, 1, bits_for_file_length)
    encoded_file_length, bmp_data = split_bytearray(bmp_data,
                                                    bits_for_file_length)

    _encode((bit_count - 1,), bmp_data, 1, 3)
    encoded_bit_count, bmp_data = split_bytearray(bmp_data, 3)

    try:
        check_data_lost_possibility(file_data, bmp_data, bit_count)
    except DataLostPossibility:
        print("Your file too large for this bmp and bit count")
        exit(4)

    _encode(file_data, bmp_data, bit_count, 8)

    header.extend(encoded_msg)
    header.extend(encoded_file_length)
    header.extend(encoded_bit_count)
    header.extend(bmp_data)

    write_to(out_file_path, header)
