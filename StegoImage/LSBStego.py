import os

from bitstring import ConstBitStream
from StegoImage import StegoImageStore

from StegoImage import StegoBinaryStore


class LSBStego:
    @staticmethod
    def save_bitplanes(image1, image2, base_dir):
        for x in range(8):
            if image1 is not None:
                bitplane = image1.create_bitplane(x)
                bitplane.save(base_dir + "/bitplane_base_" + str(x) + "." + image1.image.format)
            if image2 is not None:
                bitplane2 = image2.create_bitplane(x)
                bitplane2.save(base_dir + "/bitplane_hide_" + str(x) + "." + image2.image.format)

    def __init__(self, output_path='misc/Stego/', bitplanes_path='misc/Bitplanes/', debug_path='misc/Debug/'):
        self.output_path = output_path
        self.bitplanes_path = bitplanes_path
        self.debug_path = debug_path

    def insert_image(self, base_image_path, hidden_image_path, planes):
        steg_image = StegoImageStore.StegoImageStore(planes).load(base_image_path)
        hide_image = StegoImageStore.StegoImageStore(planes).load(hidden_image_path)
        if self.bitplanes_path is not None:
            LSBStego.save_bitplanes(steg_image, hide_image, self.bitplanes_path)
        final_image = steg_image.insert_lsb(hide_image)
        if final_image is not None:
            final_image.show()
            name, extension = os.path.splitext(os.path.basename(base_image_path))
            print("Outputting final image to: " + self.output_path + '/' + name + extension)
            final_image.save(self.output_path + '/' + name + extension)
        return final_image

    def extract_image(self, base_image_path, hidden_image_path, planes):
        steg_image = StegoImageStore.StegoImageStore(planes).load(base_image_path)
        if self.bitplanes_path is not None:
            LSBStego.save_bitplanes(steg_image, None, self.bitplanes_path)
        hidden_image = steg_image.extract_lsb()
        if hidden_image is not None:
            hidden_image.show()
            print("Outputting final image to: " + hidden_image_path)
            hidden_image.save(hidden_image_path)
        return hidden_image

    # TODO shouldn't load set the amount of channels found?
    # TODO make bitplanes to use first
    def insert_binary(self, base_image_path, hidden_data_path, planes):
        steg_image = StegoBinaryStore.StegoBinaryStore(planes).load(base_image_path)
        if self.bitplanes_path is not None:
            LSBStego.save_bitplanes(steg_image, None, self.bitplanes_path)
        data = ConstBitStream(filename=hidden_data_path)
        final_image = steg_image.insert_lsb(data)
        if final_image is not None:
            final_image.show()
            name, extension = os.path.splitext(os.path.basename(base_image_path))
            print("Outputting final image to: " + self.output_path + '/' + name + extension)
            final_image.save(self.output_path + '/' + name + extension)
        return final_image

    def extract_binary(self, base_image_path, hidden_data_path, planes):
        fp = open(hidden_data_path, "wb+")
        steg_image = StegoBinaryStore.StegoBinaryStore(planes).load(base_image_path)
        if self.bitplanes_path is not None:
            LSBStego.save_bitplanes(steg_image, None, self.bitplanes_path)
        data = steg_image.extract_lsb()
        if data is not None:
            print("Outputting final data to: " + hidden_data_path)
            data.tofile(fp)
        fp.close()
        return data
