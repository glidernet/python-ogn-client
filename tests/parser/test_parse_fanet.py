import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.aprs_comment.fanet_parser import FanetParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = FanetParser.parse_position("id1E1103CE -02fpm")

        self.assertEqual(message['address_type'], 2)
        self.assertEqual(message['aircraft_type'], 7)
        self.assertFalse(message['stealth'])
        self.assertEqual(message['address'], "1103CE")
        self.assertAlmostEqual(message['climb_rate'] * ms2fpm, -2, 0.1)

    def test_pseudo_status_comment(self):
        message = FanetParser.parse_position("")

        self.assertIsNone(message['address_type'])
        self.assertIsNone(message['aircraft_type'])
        self.assertIsNone(message['stealth'])
        self.assertIsNone(message['address'])
        self.assertIsNone(message['climb_rate'])


if __name__ == '__main__':
    unittest.main()
