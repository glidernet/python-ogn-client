import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.parse_naviter import parse


class TestStringMethods(unittest.TestCase):
    def test_OGSKYL(self):
        message = parse("id2816 +000fpm ")

        self.assertEqual(message['address'], "2816")

        self.assertAlmostEqual(message['climb_rate'] * ms2fpm, 0, 2)


if __name__ == '__main__':
    unittest.main()
