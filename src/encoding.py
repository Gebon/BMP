"""
Main module for encoding
"""
from math import ceil

from additional import read_bytearray_from_file, write_to, \
    try_get_file_header, split_bytearray, check_data_loss_possibility, \
    DataLossPossibility


SIZEOF_FILE_LENGTH_NUMBER = 32
SIZEOF_CHAR = 8
SIZEOF_USED_BITS_PER_BYTE_NUMBER = 3


def _encode_number(coded_number: int, sizeof_coded_number: int, used_bits_per_byte: int,
                   container: bytearray, invokes_count=0) -> int:
    """
    Function that encodes integer element with specififc size in bits
    (coded_element_size) into container with specified bits per byte used to encode (used_bits_per_byte)
    :param coded_number: integer value to be encoded within container
    :param sizeof_coded_number: sizeof(coded_number) in bits, e.g. for values limited with range 0..255 must be 8
    :param used_bits_per_byte: count of bits used in each byte to encode coded_element
    :param container: target bytearray which used to store encoded data
    :param invokes_count: count of this method invokes
    :return: new counter value
    """
    bytes_needed_for_encoding = round(ceil(sizeof_coded_number / used_bits_per_byte))
    shift_within_container = bytes_needed_for_encoding * invokes_count
    shift_of_coded_number = sizeof_coded_number - 1
    for j in range(bytes_needed_for_encoding):
        for i in range(used_bits_per_byte - 1, -1, -1):
            if coded_number >> shift_of_coded_number & 1:
                container[j + shift_within_container] |= 1 << i # set (8 - i)-th bit to 1
            else:
                container[j + shift_within_container] &= ~(1 << i) # set (8 - i)-th bit to 0
            shift_of_coded_number -= 1

            if shift_of_coded_number < 0:
                return invokes_count + 1


def _encode(data: [int], container: bytearray, used_bits_per_byte: int, sizeof_coded_number: int):
    """
    Function that encodes one sequence of numbers into bytearray
    :param data: source sequence
    :param container: target sequence
    :param used_bits_per_byte: see _encode_to_byte
    :param sizeof_coded_number: see _encode_to_byte
    """
    invokes_count = 0
    for number in data:
        invokes_count = _encode_number(number, sizeof_coded_number, used_bits_per_byte, container, invokes_count)


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

    msg = b'encoded'
    _encode(bytearray(msg), bmp_data, 1, SIZEOF_CHAR)
    encoded_msg, bmp_data = split_bytearray(bmp_data, len(msg)*SIZEOF_CHAR)

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
