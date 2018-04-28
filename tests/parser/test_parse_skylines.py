import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.aprs_comment.skylines_parser import SkylinesParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = SkylinesParser.parse_position("id2816 -015fpm")

        self.assertEqual(message['address'], "2816")
        self.assertAlmostEqual(message['climb_rate'] * ms2fpm, -15, 2)


if __name__ == '__main__':
    unittest.main()
