import unittest

from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS
from ogn.parser.aprs_comment.flarm_parser import FlarmParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = FlarmParser().parse_position("id21A8CBA8 -039fpm +0.1rot 3.5dB 2e -8.7kHz gps1x2 s6.09 h43 rDF0267")

        self.assertEqual(message['address_type'], 1)
        self.assertEqual(message['aircraft_type'], 8)
        self.assertFalse(message['stealth'])
        self.assertEqual(message['address'], "A8CBA8")
        self.assertAlmostEqual(message['climb_rate'], -39 * FPM_TO_MS, 2)
        self.assertEqual(message['turn_rate'], 0.1 * HPM_TO_DEGS)
        self.assertEqual(message['signal_quality'], 3.5)
        self.assertEqual(message['error_count'], 2)
        self.assertEqual(message['frequency_offset'], -8.7)
        self.assertEqual(message['gps_quality'], {'horizontal': 1, 'vertical': 2})
        self.assertEqual(message['software_version'], 6.09)
        self.assertEqual(message['hardware_version'], 67)
        self.assertEqual(message['real_address'], "DF0267")

    def test_position_comment_relevant_keys_only(self):
        # return only keys where we got informations
        message = FlarmParser().parse_position("id21A8CBA8")

        self.assertIsNotNone(message)
        self.assertEqual(sorted(message.keys()), sorted(['address_type', 'aircraft_type', 'stealth', 'address']))


if __name__ == '__main__':
    unittest.main()
