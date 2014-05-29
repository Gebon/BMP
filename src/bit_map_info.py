"""
Module with classes for BMP info
"""
__author__ = 'Галлям'

#constants
INFO_HEADER_FMT = '<IIIHHIIIIII'
V4_HEADER_FMT = '<IIIHHIIIIIIIIII36xIII'
V5_HEADER_FMT = '<IIIHHIIIIIIIIII36xIIIIIII'
RGB_QUAD_FMT = '<BBBB'
BI_RGB = 0
BI_RLE8 = 1
BI_RLE4 = 2
BI_BITFIELDS = 3
BI_JPEG = 4
BI_PNG = 5
BI_ALPHABITFIELDS = 6


class BitMapInfo:
    """
    Structure (for more see documentation in Microsoft's site)
    """
    def __init__(self, header, rgb_quad):
        self.header = header
        self.rgb_quad = rgb_quad

    def __str__(self):
        return self.header.__str__() + '\r\n\r\n' + self.rgb_quad.__str__()


class BitMapInfoHeader:
    """
    Structure (for more see documentation in Microsoft's site)
    """
    def __init__(self, info):
        self.my_size = info[0]
        self.width = info[1]
        self.height = info[2]
        self.planes = info[3]
        self.bit_count = info[4]
        self.compression_type = info[5]
        self.image_size = info[6]
        self.pixels_per_meter_x = info[7]
        self.pixels_per_meter_y = info[8]
        self.clr_used = info[9]
        self.clr_important = info[10]
        if self.compression_type == BI_RGB and \
                (self.bit_count == 16 or 32) \
                or self.bit_count == 24:
            self.colors_table_enabled = False
        else:
            self.colors_table_enabled = True

    def __str__(self):
        return 'Struct size: {0} bytes\r\n' \
               'Image width: {1} px\r\n' \
               'Image height: {2} px\r\n' \
               'Image size: {6} bytes\r\n' \
               'Bits per pixel: {3} bpp\r\n' \
               'Horizontal density: {4} ppm\r\n' \
               'Vertical density: {5} ppm\r\n' \
            .format(self.my_size, self.width, self.height, self.bit_count,
                    self.pixels_per_meter_x, self.pixels_per_meter_y,
                    self.image_size)


class BitMapV4Header(BitMapInfoHeader):
    """
    Structure (for more see documentation in Microsoft's site)
    """
    def __init__(self, info):
        BitMapInfoHeader.__init__(self, info[:-9])
        self.red_mask = info[11]
        self.green_mask = info[12]
        self.blue_mask = info[13]
        self.alpha_mask = info[14]
        self.color_space_type = info[15]
        if self.color_space_type == 0:
            self.endpoints = info[16]
            self.gamma_red = info[17]
            self.gamma_green = info[18]
            self.gamma_blue = info[19]

    def __str__(self):
        return BitMapInfoHeader.__str__(self) + '\r\n' + \
               'Red mask: {0}\r\n' \
               'Green mask: {1}\r\n' \
               'Blue mask: {2}\r\n' \
               'Alpha mask: {3}\r\n' \
               'Color space type: {4}' \
                   .format(self.red_mask, self.green_mask,
                           self.blue_mask, self.alpha_mask,
                           self.color_space_type)


class BitMapV5Header(BitMapV4Header):
    """
    Structure (for more see documentation in Microsoft's site)
    """
    def __init__(self, info):
        BitMapV4Header.__init__(self, info[:-4])
        self.intent = info[20]
        self.profile_data = info[21]
        self.profile_size = info[22]
        self.reserved = info[23]

    def __str__(self):
        return BitMapV4Header.__str__(self) + '\r\n' + \
               'Intent: {0}\r\n' \
               'Profile bmp_data: {1}\r\n' \
               'Profile size: {2}\r\n' \
                   .format(self.intent, self.profile_data, self.profile_size)


class RGBQuad:
    """
    Structure (for more see documentation in Microsoft's site)
    """
    def __init__(self, red, green, blue):
        self.rgb_red = red
        self.rgb_green = green
        self.rgb_blue = blue
        self.rgb_reserved = 0

    def __str__(self):
        return 'Red component insensitivity: {0}\r\n' \
               'Green component insensitivity: {1}\r\n' \
               'Blue component insensitivity: {2}\r\n' \
            .format(self.rgb_red, self.rgb_green, self.rgb_blue)
