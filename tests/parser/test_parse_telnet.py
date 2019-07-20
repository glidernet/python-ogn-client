import unittest
import unittest.mock as mock

from datetime import datetime

from ogn.parser.telnet_parser import parse
from ogn.parser.exceptions import ParseError


class TestStringMethods(unittest.TestCase):
    @unittest.skip("Not yet implemented")
    def test_telnet_fail_corrupt(self):
        with self.assertRaises(ParseError):
            parse('This is rubbish')

    @mock.patch('ogn.parser.telnet_parser.datetime')
    def test_telnet_parse_complete(self, datetime_mock):
        # set the utcnow-mock near to the time in the test string
        datetime_mock.utcnow.return_value = datetime(2015, 1, 1, 10, 0, 55)

        message = parse('0.181sec:868.394MHz:   1:2:DDA411 103010: [ +50.86800, +12.15279]deg  988m  +0.1m/s  25.7m/s 085.4deg  -3.5deg/sec 5 03x04m 01f_-12.61kHz  5.8/15.5dB/2 10e   30.9km 099.5deg  +1.1deg + ?     R     B8949')

        self.assertEqual(message['pps_offset'], 0.181)
        self.assertEqual(message['frequency'], 868.394)
        self.assertEqual(message['aircraft_type'], 1)
        self.assertEqual(message['address_type'], 2)
        self.assertEqual(message['address'], 'DDA411')
        self.assertEqual(message['timestamp'], datetime(2015, 1, 1, 10, 30, 10))
        self.assertEqual(message['latitude'], 50.868)
        self.assertEqual(message['longitude'], 12.15279)
        self.assertEqual(message['altitude'], 988)
        self.assertEqual(message['climb_rate'], 0.1)
        self.assertEqual(message['ground_speed'], 25.7)
        self.assertEqual(message['track'], 85.4)
        self.assertEqual(message['turn_rate'], -3.5)
        self.assertEqual(message['magic_number'], 5)  # the '5' is a magic number... 1 if ground_speed is 0.0m/s an 3 or 5 if airborne. Do you have an idea what it is?
        self.assertEqual(message['gps_status'], '03x04')
        self.assertEqual(message['channel'], 1)
        self.assertEqual(message['flarm_timeslot'], True)
        self.assertEqual(message['ogn_timeslot'], False)
        self.assertEqual(message['frequency_offset'], -12.61)
        self.assertEqual(message['decode_quality'], 5.8)
        self.assertEqual(message['signal_quality'], 15.5)
        self.assertEqual(message['demodulator_type'], 2)
        self.assertEqual(message['error_count'], 10)
        self.assertEqual(message['distance'], 30.9)
        self.assertEqual(message['bearing'], 99.5)
        self.assertEqual(message['phi'], 1.1)
        self.assertEqual(message['multichannel'], True)

    def test_telnet_parse_corrupt(self):
        message = parse('0.397sec:868.407MHz:  sA:1:784024 205656: [  +5.71003, +20.48951]deg 34012m +14.5m/s 109.7m/s 118.5deg +21.0deg/sec 0 27x40m 01_o +7.03kHz 17.2/27.0dB/2 12e 4719.5km 271.1deg  -8.5deg   ?     R     B34067')

        self.assertIsNone(message)


if __name__ == '__main__':
    unittest.main()
