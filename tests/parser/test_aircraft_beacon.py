import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.parse import parse_ogn_aircraft_beacon


class TestStringMethods(unittest.TestCase):
    def test_invalid_token(self):
        self.assertEqual(parse_ogn_aircraft_beacon("notAValidToken"), None)

    def test_basic(self):
        aircraft_beacon = parse_ogn_aircraft_beacon("id0ADDA5BA -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5 hear1084 hearB597 hearB598")

        self.assertFalse(aircraft_beacon['stealth'])
        self.assertEqual(aircraft_beacon['address'], "DDA5BA")
        self.assertAlmostEqual(aircraft_beacon['climb_rate'] * ms2fpm, -454, 2)
        self.assertEqual(aircraft_beacon['turn_rate'], -1.1)
        self.assertEqual(aircraft_beacon['signal_quality'], 8.8)
        self.assertEqual(aircraft_beacon['error_count'], 0)
        self.assertEqual(aircraft_beacon['frequency_offset'], 51.2)
        self.assertEqual(aircraft_beacon['gps_status'], '4x5')

        # self.assertEqual(len(aircraft_beacon['heared_aircraft_addresses']), 3)
        # self.assertEqual(aircraft_beacon['heared_aircraft_addresses'][0], '1084')
        # self.assertEqual(aircraft_beacon['heared_aircraft_addresses'][1], 'B597')
        # self.assertEqual(aircraft_beacon['heared_aircraft_addresses'][2], 'B598')

    def test_stealth(self):
        aircraft_beacon = parse_ogn_aircraft_beacon("id0ADD1234 -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5 hear1084 hearB597 hearB598")
        self.assertFalse(aircraft_beacon['stealth'])

        aircraft_beacon = parse_ogn_aircraft_beacon("id8ADD1234 -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5 hear1084 hearB597 hearB598")
        self.assertTrue(aircraft_beacon['stealth'])

    def test_v024(self):
        aircraft_beacon = parse_ogn_aircraft_beacon("id21400EA9 -2454fpm +0.9rot 19.5dB 0e -6.6kHz gps1x1 s6.02 h0A rDF0C56")

        self.assertEqual(aircraft_beacon['software_version'], 6.02)
        self.assertEqual(aircraft_beacon['hardware_version'], 10)
        self.assertEqual(aircraft_beacon['real_address'], "DF0C56")

    def test_v024_ogn_tracker(self):
        aircraft_beacon = parse_ogn_aircraft_beacon("id07353800 +020fpm -14.0rot FL004.43 38.5dB 0e -2.9kHz")

        self.assertEqual(aircraft_beacon['flightlevel'], 4.43)

    def test_v025(self):
        aircraft_beacon = parse_ogn_aircraft_beacon("id06DDE28D +535fpm +3.8rot 11.5dB 0e -1.0kHz gps2x3 s6.01 h0C +7.4dBm")

        self.assertEqual(aircraft_beacon['signal_power'], 7.4)


if __name__ == '__main__':
    unittest.main()
