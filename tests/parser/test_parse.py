import unittest
import unittest.mock as mock
import os

from datetime import datetime
from time import sleep

from ogn.parser.parse import parse
from ogn.parser.exceptions import AprsParseError


class TestStringMethods(unittest.TestCase):
    def parse_valid_beacon_data_file(self, filename, beacon_type):
        with open(os.path.dirname(__file__) + '/valid_beacon_data/' + filename) as f:
            for line in f:
                if not line[0] == '#':
                    try:
                        message = parse(line, datetime(2015, 4, 10, 17, 0))
                        self.assertFalse(message is None)
                        self.assertEqual(message['beacon_type'], beacon_type)
                    except NotImplementedError as e:
                        print(e)

    def test_aprs_aircraft_beacons(self):
        self.parse_valid_beacon_data_file(filename='aprs_aircraft.txt', beacon_type='aircraft_beacon')

    def test_aprs_receiver_beacons(self):
        self.parse_valid_beacon_data_file(filename='aprs_receiver.txt', beacon_type='receiver_beacon')

    def test_ogn_flarm_beacons(self):
        self.parse_valid_beacon_data_file(filename='ogn_flarm.txt', beacon_type='aircraft_beacon')

    def test_ogn_receiver_beacons(self):
        self.parse_valid_beacon_data_file(filename='ogn_receiver.txt', beacon_type='receiver_beacon')

    def test_ogn_tracker_beacons(self):
        self.parse_valid_beacon_data_file(filename='ogn_tracker.txt', beacon_type='aircraft_beacon')

    def test_lt24_beacons(self):
        self.parse_valid_beacon_data_file(filename='lt24.txt', beacon_type='lt24_beacon')

    def test_naviter_beacons(self):
        self.parse_valid_beacon_data_file(filename='naviter.txt', beacon_type='naviter_beacon')

    def test_skylines_beacons(self):
        self.parse_valid_beacon_data_file(filename='skylines.txt', beacon_type='skylines_beacon')

    def test_spider_beacons(self):
        self.parse_valid_beacon_data_file(filename='spider.txt', beacon_type='spider_beacon')

    def test_spot_beacons(self):
        self.parse_valid_beacon_data_file(filename='spot.txt', beacon_type='spot_beacon')

    def test_fail_parse_aprs_none(self):
        with self.assertRaises(TypeError):
            parse(None)

    def test_fail_empty(self):
        with self.assertRaises(AprsParseError):
            parse("")

    def test_fail_bad_string(self):
        with self.assertRaises(AprsParseError):
            parse("Lachens>APRS,TCPIwontbeavalidstring")

    def test_v026_chile(self):
        # receiver beacons from chile have a APRS position message with a pure user comment
        message = parse("VITACURA1>APRS,TCPIP*,qAC,GLIDERN4:/201146h3322.79SI07034.80W&/A=002329 Vitacura Municipal Aerodrome, Club de Planeadores Vitacura", reference_date=datetime(2015, 1, 1))

        self.assertEqual(message['user_comment'], "Vitacura Municipal Aerodrome, Club de Planeadores Vitacura")

    @mock.patch('ogn.parser.parse_module.createTimestamp')
    def test_default_reference_date(self, createTimestamp_mock):
        valid_aprs_string = "Lachens>APRS,TCPIP*,qAC,GLIDERN2:/165334h4344.70NI00639.19E&/A=005435 v0.2.1 CPU:0.3 RAM:1764.4/2121.4MB NTP:2.8ms/+4.9ppm +47.0C RF:+0.70dB"

        parse(valid_aprs_string)
        call_args_before = createTimestamp_mock.call_args

        sleep(1)

        parse(valid_aprs_string)
        call_args_seconds_later = createTimestamp_mock.call_args

        self.assertNotEqual(call_args_before, call_args_seconds_later)

    def test_copy_constructor(self):
        valid_aprs_string = "FLRDDA5BA>APRS,qAS,LFMX:/160829h4415.41N/00600.03E'342/049/A=005524 id0ADDA5BA -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5"
        message = parse(valid_aprs_string, reference_date=datetime(2015, 1, 1, 16, 8, 29))

        self.assertEqual(message['name'], 'FLRDDA5BA')
        self.assertEqual(message['address'], 'DDA5BA')


if __name__ == '__main__':
    unittest.main()
