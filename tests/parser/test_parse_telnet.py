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
    def test_telnet_parse(self, datetime_mock):
        # set the utcnow-mock near to the time in the test string
        datetime_mock.utcnow.return_value = datetime(2015, 1, 1, 10, 0, 55)

        message = parse('0.867sec:868.398MHz:   1:2:DD9AB2 100050: [ +47.44356, +11.77856]deg 2749m  +3.2m/s  34.5m/s 082.7deg  -0.7deg/sec 5 03x03m  -1.6kHz  8.5dB  1e   50.6km 151.4deg  +1.9deg')

        self.assertEqual(message['pps_offset'], 0.867)
        self.assertEqual(message['frequency'], 868.398)
        self.assertEqual(message['aircraft_type'], 1)
        self.assertEqual(message['address_type'], 2)
        self.assertEqual(message['address'], 'DD9AB2')
        self.assertEqual(message['timestamp'], datetime(2015, 1, 1, 10, 0, 50))
        self.assertEqual(message['latitude'], 47.44356)
        self.assertEqual(message['longitude'], 11.77856)
        self.assertEqual(message['altitude'], 2749)
        self.assertEqual(message['climb_rate'], 3.2)
        self.assertEqual(message['ground_speed'], 34.5)
        self.assertEqual(message['track'], 82.7)
        self.assertEqual(message['turn_rate'], -0.7)
        self.assertEqual(message['magic_number'], 5)  # the '5' is a magic number... 1 if ground_speed is 0.0m/s an 3 or 5 if airborne. Do you have an idea what it is?
        self.assertEqual(message['gps_status'], '03x03')
        self.assertEqual(message['frequency_offset'], -1.6)
        self.assertEqual(message['signal_quality'], 8.5)
        self.assertEqual(message['error_count'], 1)
        self.assertEqual(message['distance'], 50.6)
        self.assertEqual(message['bearing'], 151.4)
        self.assertEqual(message['phi'], 1.9)


if __name__ == '__main__':
    unittest.main()
