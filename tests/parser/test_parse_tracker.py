import unittest

from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS
from ogn.parser.aprs_comment.tracker_parser import TrackerParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = TrackerParser.parse_position("id072FD00F -058fpm +1.1rot FL003.12 32.8dB 0e -0.8kHz gps3x5 +12.7dBm")

        self.assertEqual(message['address_type'], 3)
        self.assertEqual(message['aircraft_type'], 1)
        self.assertFalse(message['stealth'])
        self.assertEqual(message['address'], "2FD00F")
        self.assertAlmostEqual(message['climb_rate'], -58 * FPM_TO_MS, 2)
        self.assertEqual(message['turn_rate'], 1.1 * HPM_TO_DEGS)
        self.assertEqual(message['flightlevel'], 3.12)
        self.assertEqual(message['signal_quality'], 32.8)
        self.assertEqual(message['error_count'], 0)
        self.assertEqual(message['frequency_offset'], -0.8)
        self.assertEqual(message['gps_quality'], {'horizontal': 3, 'vertical': 5})
        self.assertEqual(message['signal_power'], 12.7)

    def test_status_comment(self):
        message = TrackerParser.parse_status("h00 v00 9sat/1 164m 1002.6hPa +20.2degC 0% 3.34V 14/-110.5dBm 1/min")

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

    def test_no_hw_version(self):
        # Full live message without hardware version:
        # "ICA38C6FB>APRS,qAS,LFNZ:/101313h4346.25N/00453.67E'355/042/A=001161 !W15! id0538C6FB +1723fpm +0.1rot 20.0dB 0e -8.0kHz gps1x1"
        message = TrackerParser.parse_position("id0538C6FB +1723fpm +0.1rot 20.0dB 0e -8.0kHz gps1x1")
        self.assertEqual(message['address_type'], 1)
        self.assertEqual(message['aircraft_type'], 1)
        self.assertFalse(message['stealth'])
        self.assertEqual(message['address'], "38C6FB")
        self.assertAlmostEqual(message['climb_rate'], 1723 * FPM_TO_MS, 2)
        self.assertEqual(message['turn_rate'], 0.1 * HPM_TO_DEGS)
        self.assertEqual(message['signal_quality'], 20.0)
        self.assertEqual(message['error_count'], 0)
        self.assertEqual(message['frequency_offset'], -8.0)
        self.assertEqual(message['gps_quality'], {'horizontal': 1, 'vertical': 1})

if __name__ == '__main__':
    unittest.main()
