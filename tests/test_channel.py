import unittest

from StegoImage import Channel


class TestChannel(unittest.TestCase):
    def test_insert(self):
        test_channel = Channel()
        self.assertEqual(test_channel.value(), 0)

        test_channel.insert(1)
        self.assertEqual(test_channel.value(), 4)

        test_channel.insert(0)
        self.assertEqual(test_channel.value(), 4)

        test_channel.insert(1)
        self.assertEqual(test_channel.value(), 5)

        returned = test_channel.insert(1)
        self.assertEqual(returned, False)
        self.assertEqual(test_channel.value(), 5)

    def test_extract(self):
        test_channel = Channel(164)
        value = test_channel.extract()
        self.assertEqual(value, 1)

        value = test_channel.extract()
        self.assertEqual(value, 0)

        value = test_channel.extract()
        self.assertEqual(value, 0)

        value = test_channel.extract()
        self.assertEqual(value, None)

if __name__ == '__main__':
    unittest.main()
