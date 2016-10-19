from PIL import Image
from bitstring import Bits
from .BaseStegoImage import BaseStegoImage
from .Channel import Channel


class StegoImageStore(BaseStegoImage):
    def __init__(self, nbr_of_planes=3):
        super().__init__(nbr_of_planes)
        self.__get_lsb_mask = (2 ** self._nbr_of_planes - 1) << (self._bits_per_channel - self._nbr_of_planes)

    def _insert_header(self, width, height):
        width_h = Bits(uint=width, length=self._header_reserved_size // 2)
        height_h = Bits(uint=height, length=self._header_reserved_size // 2)
        header = width_h + height_h
        return self._insert_data(header)

    def _insert_image(self, image):
        start = self._channel_pos
        for channel in image.channels:
            channel_bits = (channel.value() & self.__get_lsb_mask) >> (self._bits_per_channel -
                                                                       self._nbr_of_planes)

            channel_bits = Bits(uint=channel_bits, length=self._nbr_of_planes)
            self._insert_data(channel_bits)
        return self._channel_pos - start

    def _extract_header(self):
        width_h = self._extract_data(self._header_reserved_size // 2)
        height_h = self._extract_data(self._header_reserved_size // 2)
        return width_h.uint, height_h.uint

    def _extract_image_channels(self, width, height):
        image_data = self._extract_data((width * height) * self._bits_per_channel)
        bit_shift = self._bits_per_channel - self._nbr_of_planes
        channels = []
        for x in range(0, image_data.len, self._nbr_of_planes):
            channel_bits = image_data[x:x + self._nbr_of_planes].uint << bit_shift
            extracted_channel = Channel(channel_bits, self._bits_per_channel, self._nbr_of_planes)
            channels.append(extracted_channel)
        if len(channels) != ((width * height) * self._bits_per_channel) // self._nbr_of_planes:
            print("Warning: Extracted bits do not correspond to expected size")
        return channels

    def verify_lsb(self, data):
        bits_to_encode = (len(data.channels) * self._nbr_of_planes) + self._header_reserved_size
        bits_available = len(self.channels) * self._nbr_of_planes
        if bits_to_encode > bits_available:
            print("Error: More data to hide than space available in base image")
            return False
        return True

    # data : BaseStegoImage
    def insert_lsb(self, data):
        if self.verify_lsb(data):
            width, height = data.image.size
            self._insert_header(width, height)
            self._insert_image(data)
            pixels = self._pack_pixels(self._nbr_of_channels, self.image.size[0], self.image.size[1], self.channels)
            stego_image = Image.new(self.image.mode, self.image.size)
            stego_image.putdata(pixels)
            return stego_image
        return None

    def extract_lsb(self):
        width, height = self._extract_header()
        if width <= 0 or height <= 0:
            print("Invalid Stego Data: Invalid image size stored in image.")
            return None
        channels = self._extract_image_channels(width, height)
        # self.debug_image_extract_lsb("hidden_image.debug", channels)
        pixels = self._pack_pixels(self._nbr_of_channels, width, height, channels)
        hidden_image = Image.new(self.image.mode, (width, height))
        hidden_image.putdata(pixels)
        return hidden_image

    def debug_image_insert_lsb(self, path, channels):
        debug_file = open(path, "w")
        x = 0
        debug_file.write("Channel value insert_value\n")
        for channel in channels:
            channel_bits = (channel.value() & self.__get_lsb_mask) >> (self._bits_per_channel -
                                                                       self._nbr_of_planes)
            debug_file.write(str(x) + " " + format(channel.value(), "#010b") + " " + format(channel_bits, "#010b") +
                             "\n")
            x += 1
        debug_file.close()

    def debug_image_extract_lsb(self, path, channels):
        debug_file = open(path, "w")
        x = 0
        debug_file.write("Channel value insert_value\n")
        for channel in channels:
            extracted_bits = channel.value() >> (self._bits_per_channel - self._nbr_of_planes)
            debug_file.write(str(x) + " " + format(channel.value(), "#010b") + " " + format(extracted_bits, "#010b") +
                             '\n')
            x += 1
