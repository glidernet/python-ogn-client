import unittest

from ogn.parser.utils import FPM_TO_MS
from ogn.parser.aprs_comment.fanet_parser import FanetParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = FanetParser().parse_position("id1E1103CE -02fpm")

        self.assertEqual(message['address_type'], 2)
        self.assertEqual(message['aircraft_type'], 7)
        self.assertFalse(message['stealth'])
        self.assertEqual(message['address'], "1103CE")
        self.assertAlmostEqual(message['climb_rate'], -2 * FPM_TO_MS, 0.1)

    def test_pseudo_status_comment(self):
        message = FanetParser().parse_position("")

        self.assertEqual(message, {})

    def test_v028_status(self):
        message = FanetParser().parse_status('Name="Juerg Zweifel" 15.0dB -17.1kHz 1e')

        self.assertEqual(message['fanet_name'], "Juerg Zweifel")
        self.assertEqual(message['signal_quality'], 15.0)
        self.assertEqual(message['frequency_offset'], -17.1)
        self.assertEqual(message['error_count'], 1)


if __name__ == '__main__':
    unittest.main()
