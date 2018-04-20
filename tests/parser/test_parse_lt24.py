import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.aprs_comment.lt24_parser import LT24Parser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = LT24Parser.parse_position("id25387 +000fpm GPS")

        self.assertEqual(message['id'], "25387")
        self.assertAlmostEqual(message['climb_rate'] * ms2fpm, 0, 2)
        self.assertEqual(message['source'], 'GPS')


if __name__ == '__main__':
    unittest.main()
