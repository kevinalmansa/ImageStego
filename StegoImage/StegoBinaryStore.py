from PIL import Image
from bitstring import Bits

from StegoImage.BaseStegoImage import BaseStegoImage


class StegoBinaryStore(BaseStegoImage):
    def __init__(self, nbr_of_planes=3):
        super().__init__(nbr_of_planes)

    def _insert_header(self, data_size):
        header = Bits(uint=data_size, length=self._header_reserved_size)
        return self._insert_data(header)

    def verify_lsb(self, data):
        bits_to_encode = data.len
        bits_available = len(self.channels) * self._nbr_of_planes
        if bits_to_encode > bits_available:
            print("Error: More data to hide than space available in base image")
            return False
        return True

    def insert_lsb(self, data):
        if self.verify_lsb(data):
            self._insert_header(data.len // 8)
            self._insert_data(data)
            pixels = self._pack_pixels(self._nbr_of_channels, self.image.size[0], self.image.size[1], self.channels)
            stego_image = Image.new(self.image.mode, self.image.size)
            stego_image.putdata(pixels)
            return stego_image
        return None

    def extract_lsb(self):
        size = self._extract_data(self._header_reserved_size)
        if size.uint <= 0:
            print("Invalid Stego Data: Invalid image size stored in image.")
            return None
        data = self._extract_data(size.uint * 8)
        return data
