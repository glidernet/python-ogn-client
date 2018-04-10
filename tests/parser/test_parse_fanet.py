import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.aprs_comment.fanet_parser import FanetParser


class TestStringMethods(unittest.TestCase):
    def test_regular_beacon(self):
        message = FanetParser.parse_position("id1E1103CE -02fpm")

        self.assertEqual(message['id'], "1E1103CE")
        self.assertAlmostEqual(message['climb_rate'] * ms2fpm, -2, 0.1)

    def test_pseudo_status_beacon(self):
        message = FanetParser.parse_position("")

        self.assertIsNone(message['id'])
        self.assertIsNone(message['climb_rate'])


if __name__ == '__main__':
    unittest.main()
