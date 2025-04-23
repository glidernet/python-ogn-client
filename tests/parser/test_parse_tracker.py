import unittest

from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS
from ogn.parser.aprs_comment.tracker_parser import TrackerParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = TrackerParser().parse_position("id072FD00F -058fpm +1.1rot FL003.12 32.8dB 0e -0.8kHz gps3x5 +12.7dBm")

        assert message['address_type'] == 3
        assert message['aircraft_type'] == 1
        self.assertFalse(message['stealth'])
        assert message['address'] == "2FD00F"
        self.assertAlmostEqual(message['climb_rate'], -58 * FPM_TO_MS, 2)
        assert message['turn_rate'] == 1.1 * HPM_TO_DEGS
        assert message['flightlevel'] == 3.12
        assert message['signal_quality'] == 32.8
        assert message['error_count'] == 0
        assert message['frequency_offset'] == -0.8
        assert message['gps_quality'] == {'horizontal': 3, 'vertical': 5}
        assert message['signal_power'] == 12.7

    def test_status_comment(self):
        message = TrackerParser().parse_status("h00 v00 9sat/1 164m 1002.6hPa +20.2degC 0% 3.34V 14/-110.5dBm 1/min")

        assert message['hardware_version'] == 0
        assert message['software_version'] == 0
        assert message['gps_satellites'] == 9
        assert message['gps_quality'] == 1
        assert message['gps_altitude'] == 164
        assert message['pressure'] == 1002.6
        assert message['temperature'] == 20.2
        assert message['humidity'] == 0
        assert message['voltage'] == 3.34
        assert message['transmitter_power'] == 14
        assert message['noise_level'] == -110.5
        assert message['relays'] == 1

    def test_status_comment_comment(self):
        message = TrackerParser().parse_status("Pilot=Pawel Hard=DIY/STM32")

        assert message['comment'] == "Pilot=Pawel Hard=DIY/STM32"


if __name__ == '__main__':
    unittest.main()
