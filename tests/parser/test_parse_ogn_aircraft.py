import unittest

from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS
from ogn.parser.aprs_comment.ogn_parser import OgnParser


class TestStringMethods(unittest.TestCase):
    def test_invalid_token(self):
        self.assertEqual(OgnParser().parse_aircraft_beacon("notAValidToken"), None)

    def test_basic(self):
        message = OgnParser().parse_aircraft_beacon("id0ADDA5BA -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5 hear1084 hearB597 hearB598")

        self.assertEqual(message['address_type'], 2)
        self.assertEqual(message['aircraft_type'], 2)
        self.assertFalse(message['stealth'])
        self.assertEqual(message['address'], "DDA5BA")
        self.assertAlmostEqual(message['climb_rate'], -454 * FPM_TO_MS, 2)
        self.assertEqual(message['turn_rate'], -1.1 * HPM_TO_DEGS)
        self.assertEqual(message['signal_quality'], 8.8)
        self.assertEqual(message['error_count'], 0)
        self.assertEqual(message['frequency_offset'], 51.2)
        self.assertEqual(message['gps_quality'], {'horizontal': 4, 'vertical': 5})
        self.assertEqual(len(message['proximity']), 3)
        self.assertEqual(message['proximity'][0], '1084')
        self.assertEqual(message['proximity'][1], 'B597')
        self.assertEqual(message['proximity'][2], 'B598')

    def test_stealth(self):
        message = OgnParser().parse_aircraft_beacon("id0ADD1234 -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5 hear1084 hearB597 hearB598")
        self.assertFalse(message['stealth'])

        message = OgnParser().parse_aircraft_beacon("id8ADD1234 -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5 hear1084 hearB597 hearB598")
        self.assertTrue(message['stealth'])

    def test_v024(self):
        message = OgnParser().parse_aircraft_beacon("id21400EA9 -2454fpm +0.9rot 19.5dB 0e -6.6kHz gps1x1 s6.02 h0A rDF0C56")

        self.assertEqual(message['software_version'], 6.02)
        self.assertEqual(message['hardware_version'], 10)
        self.assertEqual(message['real_address'], "DF0C56")

    def test_v024_ogn_tracker(self):
        message = OgnParser().parse_aircraft_beacon("id07353800 +020fpm -14.0rot FL004.43 38.5dB 0e -2.9kHz")

        self.assertEqual(message['flightlevel'], 4.43)

    def test_v025(self):
        message = OgnParser().parse_aircraft_beacon("id06DDE28D +535fpm +3.8rot 11.5dB 0e -1.0kHz gps2x3 s6.01 h0C +7.4dBm")

        self.assertEqual(message['signal_power'], 7.4)

    def test_v026(self):
        # from 0.2.6 it is sufficent we have only the ID, climb and turn rate or just the ID
        message_triple = OgnParser().parse_aircraft_beacon("id093D0930 +000fpm +0.0rot")
        message_single = OgnParser().parse_aircraft_beacon("id093D0930")

        self.assertIsNotNone(message_triple)
        self.assertIsNotNone(message_single)

    def test_relevant_keys_only(self):
        # return only keys where we got informations
        message = OgnParser().parse_aircraft_beacon("id093D0930")

        self.assertIsNotNone(message)
        self.assertEqual(sorted(message.keys()), sorted(['address_type', 'aircraft_type', 'stealth', 'address']))


if __name__ == '__main__':
    unittest.main()
