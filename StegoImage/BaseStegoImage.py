from PIL import Image
from bitstring import BitArray
from .Channel import Channel


class BaseStegoImage:
    @staticmethod
    def _pack_pixels(nbr_of_channels, width, height, data):
        if nbr_of_channels > 1:
            pixels = []
            for x in range(0, width * height, nbr_of_channels):
                pixel_channels = data[x:x+nbr_of_channels]
                pixel_raw = [pixel_channels[channel_itr].value() for channel_itr in range(nbr_of_channels)]
                pixels.append(tuple(pixel_raw))
        else:
            pixels = [data[x].value() for x in range(0, width * height, nbr_of_channels)]
        return pixels

    # data : Bits or BitArray
    def _insert_data(self, data):
        for bit in data:
            if not self.channels[self._channel_pos].insert(bit):
                self._channel_pos += 1
                self.channels[self._channel_pos].insert(bit)
        return data.len

    def _extract_data(self, size):
        data = BitArray()
        for x in range(size):
            bit = self.channels[self._channel_pos].extract()
            if bit is None:
                self._channel_pos += 1
                bit = self.channels[self._channel_pos].extract()
            bs = BitArray(uint=bit, length=1)
            data.append(bs)
        return data

    def __init__(self, nbr_of_planes=3):
        # Image specifics
        self._bits_per_channel = 8
        self._header_reserved_size = 32  # in bits
        self._nbr_of_channels = 0
        self._nbr_of_planes = nbr_of_planes
        # Actual image data
        self.image = None
        self.path = ''
        self.channels = None
        self._channel_pos = 0

    def __unpack_pixels(self):
        # Retrieve the PIL image pixels (format from PIL: pixels[width, height])
        pixels = self.image.load()
        width, height = self.image.size
        self.channels = []
        # If the pixel has multiple channels
        if type(pixels[0, 0]) == tuple:
            self._nbr_of_channels = len(pixels[0, 0])
            for y in range(height):
                for x in range(width):
                    for channel_nbr in range(len(pixels[x, y])):
                        raw_channel = pixels[x, y][channel_nbr]
                        self.channels.append(Channel(raw_channel, self._bits_per_channel, self._nbr_of_planes))
        elif type(pixels[0, 0]) == int:
            self._nbr_of_channels = 1
            for y in range(height):
                for x in range(width):
                    raw_channel = pixels[x, y]
                    self.channels.append(Channel(raw_channel, self._bits_per_channel, self._nbr_of_planes))

    def debug_image_info(self):
        print("Image Info <" + self.path + ">:")
        print(self.image.format, self.image.size, self.image.mode)

    def load(self, path):
        self.path = path
        self.image = Image.open(path)
        self.__unpack_pixels()
        self.debug_image_info()
        return self

    def set_image(self, path, image):
        self.path = path
        self.image = image
        self.__unpack_pixels()
        self.debug_image_info()
        return self

    def save(self, path):
        # pixels = self._pack_pixels(self._nbr_of_channels, self.image.size[0], self.image.size[1], self.channels)
        # stego_image = Image.new(self.image.mode, self.image.size)
        # stego_image.putdata(pixels)
        # stego_image.image.save(path)
        self.image.save(path)
        return self.image

    def create_bitplane(self, plane=0):
        if self.channels is None:
            return None
        plane_mask = 1 << plane
        width, height = self.image.size
        pixel_plane = []
        for channel in self.channels:
            cur_channel = Channel(channel.value() & plane_mask, self._bits_per_channel, self._nbr_of_planes)
            if cur_channel.value() > 0:
                cur_channel.set(255)
            pixel_plane.append(cur_channel)
        pixels = self._pack_pixels(self._nbr_of_channels, width, height, pixel_plane)
        plane_image = Image.new(self.image.mode, self.image.size)
        plane_image.putdata(pixels)
        return plane_image

    def verify_lsb(self, data):
        raise NotImplementedError

    def insert_lsb(self, data):
        raise NotImplementedError

    def extract_lsb(self):
        raise NotImplementedError
