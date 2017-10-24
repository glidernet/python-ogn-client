import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.parse_naviter import parse


class TestStringMethods(unittest.TestCase):
    def test_OGLT24(self):
        message = parse("id25387 +001fpm GPS ")

        self.assertEqual(message['address'], "25387")

        self.assertAlmostEqual(message['climb_rate'] * ms2fpm, 1, 1)


if __name__ == '__main__':
    unittest.main()
