import unittest

from ogn.parser.utils import FPM_TO_MS
from ogn.parser.aprs_comment.lt24_parser import LT24Parser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = LT24Parser().parse_position("id25387 +123fpm GPS")

        self.assertEqual(message['lt24_id'], "25387")
        self.assertAlmostEqual(message['climb_rate'], 123 * FPM_TO_MS, 2)
        self.assertEqual(message['source'], 'GPS')


if __name__ == '__main__':
    unittest.main()
