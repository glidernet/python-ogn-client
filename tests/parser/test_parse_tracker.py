import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.parse_tracker import parse_position, parse_status


class TestStringMethods(unittest.TestCase):
    def test_position_beacon(self):
        message = parse_position("id072FD00F -058fpm +1.1rot FL003.12 32.8dB 0e -0.8kHz gps3x5")

        self.assertEqual(message['address_type'], 3)
        self.assertEqual(message['aircraft_type'], 1)
        self.assertFalse(message['stealth'])
        self.assertEqual(message['address'], "2FD00F")
        self.assertAlmostEqual(message['climb_rate'] * ms2fpm, -58, 2)
        self.assertEqual(message['turn_rate'], 1.1)
        self.assertEqual(message['flightlevel'], 3.12)
        self.assertEqual(message['signal_quality'], 32.8)
        self.assertEqual(message['error_count'], 0)
        self.assertEqual(message['frequency_offset'], -0.8)
        self.assertEqual(message['gps_status'], '3x5')

    def test_status(self):
        message = parse_status("h00 v00 9sat/1 164m 1002.6hPa +20.2degC 0% 3.34V 14/-110.5dBm 1/min")

        self.assertEqual(message['hardware_version'], 0)
        self.assertEqual(message['software_version'], 0)
        self.assertEqual(message['gps_satellites'], 9)
        self.assertEqual(message['gps_quality'], 1)
        self.assertEqual(message['gps_altitude'], 164)
        self.assertEqual(message['pressure'], 1002.6)
        self.assertEqual(message['temperature'], 20.2)
        self.assertEqual(message['humidity'], 0)
        self.assertEqual(message['voltage'], 3.34)
        self.assertEqual(message['transmitter_power'], 14)
        self.assertEqual(message['noise_level'], -110.5)
        self.assertEqual(message['relays'], 1)


if __name__ == '__main__':
    unittest.main()
