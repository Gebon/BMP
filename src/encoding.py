"""
Main module for encoding
"""
from math import ceil

from additional import read_bytearray_from_file, write_to, \
    try_get_file_header, split_bytearray, check_data_loss_possibility, \
    DataLossPossibility
from constants import SIZEOF_FILE_LENGTH_NUMBER, SIZEOF_CHAR, SIZEOF_USED_BITS_PER_BYTE_NUMBER, \
    MSG_ENCODED


def _encode_number_into_another_number(coded_number, container_number, used_bits_per_byte, shift_of_coded_number):
    """
    Function that encodes number into container number with specified bits per byte used to encode (used_bits_per_byte)
    :param coded_number: integer value to be encoded within container
    :param used_bits_per_byte: count of bits used in each byte to encode coded_element
    :param container_number: target number which used to store encoded data
    :param shift_of_coded_number: specifies which part of number should be encoded into container
    :return: tuple (container_number, shift_of_coded_number), where container_number already contains encoded data
    """
    shift_within_container_number = used_bits_per_byte - 1
    while shift_of_coded_number >= 0 and shift_within_container_number >= 0:
        if coded_number >> shift_of_coded_number & 1:
            container_number |= 1 << shift_within_container_number  # set (8 - i)-th bit to 1
        else:
            container_number &= ~(1 << shift_within_container_number)  # set (8 - i)-th bit to 0
        shift_of_coded_number -= 1
        shift_within_container_number -= 1

    return container_number, shift_of_coded_number


def _encode(data: [int], container: bytearray, used_bits_per_byte: int, sizeof_coded_number: int):
    """
    Function that encodes one sequence of numbers into bytearray
    :param data: source sequence
    :param container: target sequence
    :param used_bits_per_byte: see _encode_to_byte
    :param sizeof_coded_number: see _encode_to_byte
    """
    count_of_bytes_needed_for_encoding_one_number = round(ceil(sizeof_coded_number / used_bits_per_byte))
    for i, coded_number in enumerate(data):
        shift_within_container = count_of_bytes_needed_for_encoding_one_number * i
        shift_of_coded_number = sizeof_coded_number - 1
        for j in range(count_of_bytes_needed_for_encoding_one_number):
            container[j + shift_within_container], shift_of_coded_number = \
                _encode_number_into_another_number(coded_number, container[j + shift_within_container],
                                                   used_bits_per_byte, shift_of_coded_number)

            if shift_of_coded_number < 0:
                break


def encode(bmp_file_path, file_to_encode_path, out_file_path, bit_count=1):
    """
    Encode some file into BMP file and record result to out_file_path
    :param bmp_file_path: path to BMP file
    :param file_to_encode_path: path to file to be encoded
    :param out_file_path: path to output BMP file
    :param bit_count: bits used to encode per byte
    """
    bmp_data = read_bytearray_from_file(bmp_file_path)
    file_data = read_bytearray_from_file(file_to_encode_path)

    file_header = try_get_file_header(bmp_data)

    header, bmp_data = split_bytearray(bmp_data, file_header.off_bits)

    _encode(bytearray(MSG_ENCODED), bmp_data, 1, SIZEOF_CHAR)
    encoded_msg, bmp_data = split_bytearray(bmp_data, len(MSG_ENCODED) * SIZEOF_CHAR)

    file_length = len(file_data)
    _encode((file_length,), bmp_data, 1, SIZEOF_FILE_LENGTH_NUMBER)
    encoded_file_length, bmp_data = split_bytearray(bmp_data,
                                                    SIZEOF_FILE_LENGTH_NUMBER)

    _encode((bit_count - 1,), bmp_data, 1, SIZEOF_USED_BITS_PER_BYTE_NUMBER)
    encoded_bit_count, bmp_data = split_bytearray(bmp_data, SIZEOF_USED_BITS_PER_BYTE_NUMBER)

    try:
        check_data_loss_possibility(file_data, bmp_data, bit_count)
    except DataLossPossibility:
        print("Your file too large for this bmp and bit count")
        exit(4)

    _encode(file_data, bmp_data, bit_count, 8)

    header.extend(encoded_msg)
    header.extend(encoded_file_length)
    header.extend(encoded_bit_count)
    header.extend(bmp_data)

    write_to(out_file_path, header)
