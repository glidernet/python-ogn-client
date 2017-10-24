import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.parse_naviter import parse


class TestStringMethods(unittest.TestCase):
    def test_OGSPID(self):
        message = parse("id300234010617040 +19dB LWE 3D ")

        self.assertEqual(message['address'], "617040")
        self.assertEqual(message['signal_quality'], "19")



if __name__ == '__main__':
    unittest.main()
