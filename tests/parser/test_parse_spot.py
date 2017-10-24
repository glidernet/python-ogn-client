import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.parse_naviter import parse


class TestStringMethods(unittest.TestCase):
    def test_OGSPOT(self):
        message = parse("id0-2860357 SPOT3 GOOD ")
        self.assertEqual(message['address'], "042121")


if __name__ == '__main__':
    unittest.main()
