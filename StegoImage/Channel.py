class Channel:
    # value: Value of channel, max is 2**bits_per_channel - 1 TODO add verification to code
    # bits_per_channel : Number of bits in a pixel channel, default is 8
    # planes : The number of planes to use in the pixel channel for storing data using LSB
    def __init__(self, value=0, bits_per_channel=8, planes=3):
        # Value of channel, max is 2**bits_per_channel - 1
        self._val = value
        # Position in planes for storing or reading data, max value is planes - 1
        self._pos = 0
        self._planes = planes
        self._bits_per_channel = bits_per_channel
        # Bit mask used for setting a specific bit in _val
        self._set_hidden_data_mask = (2**bits_per_channel) - 1

    def value(self):
        return self._val

    def set(self, value):
        self._val = value
        self._pos = 0

    # This can be used to reread hidden information, or overwrite the channel
    def reset_position(self):
        self._pos = 0

    def insert(self, bit):
        if self._pos < self._planes:
            # Binary Mask calculated based on position and planes
            # used to clear the bit that is being set (ex. 255 ^ bit_to_set, 255 = 2**bits_per_channel - 1)
            bit_to_set_mask = 1 << ((self._planes - 1) - self._pos)
            # Align bit for placement in _val
            value_to_set = bit << ((self._planes - 1) - self._pos)
            # Clear the appropriate bit in _val and assign the bit to insert
            self._val = self._val & (self._set_hidden_data_mask ^ bit_to_set_mask) | value_to_set
            # Increment position, as the previous is now used
            self._pos += 1
            return True
        return False

    def extract(self):
        if self._pos < self._planes:
            # Binary Mask calculated based on position and planes used to retrieve the bit at position self._pos
            bit_to_recover = 1 << ((self._planes - 1) - self._pos)
            # Use the mask bit_to_recover to retrieve the bit, every other bit value will be 0
            value = self._val & bit_to_recover
            # We want to know if that bit is a 0 or 1, so shift it as necessary
            value >>= (self._planes - 1) - self._pos
            # Increment position, as the value is now retrieved
            self._pos += 1
            # Bool, 0 False or 1 True, is smaller than an int
            return bool(value)
        return None
