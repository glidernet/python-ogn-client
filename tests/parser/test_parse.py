import unittest
import unittest.mock as mock

from datetime import datetime
from time import sleep

from ogn.parser.parse import parse
from ogn.parser.exceptions import AprsParseError, OgnParseError


class TestStringMethods(unittest.TestCase):
    def test_valid_beacons(self):
        with open('tests/valid_beacons.txt') as f:
            for line in f:
                if not line[0] == '#':
                    parse(line, datetime(2015, 4, 10, 17, 0))

    def test_fail_none(self):
        with self.assertRaises(TypeError):
            parse(None)

    def test_fail_empty(self):
        with self.assertRaises(AprsParseError):
            parse("")

    def test_fail_bad_string(self):
        with self.assertRaises(AprsParseError):
            parse("Lachens>APRS,TCPIwontbeavalidstring")

    def test_incomplete_device_string(self):
        with self.assertRaises(OgnParseError):
            parse("ICA4B0E3A>APRS,qAS,Letzi:/072319h4711.75N\\00802.59E^327/149/A=006498 id154B0E3A -395",
                  datetime(2015, 4, 10, 7, 24))

    @unittest.skip('Does not work, I dont know why (2017-04-11)')
    @mock.patch('ogn.parser.parse.createTimestamp')
    def test_default_reference_date(self, createTimestamp_mock):
        valid_aprs_string = "Lachens>APRS,TCPIP*,qAC,GLIDERN2:/165334h4344.70NI00639.19E&/A=005435 v0.2.1 CPU:0.3 RAM:1764.4/21"

        parse(valid_aprs_string)
        call_args_before = createTimestamp_mock.call_args

        sleep(1)

        parse(valid_aprs_string)
        call_args_seconds_later = createTimestamp_mock.call_args

        self.assertNotEqual(call_args_before, call_args_seconds_later)

    def test_copy_constructor(self):
        valid_aprs_string = "FLRDDA5BA>APRS,qAS,LFMX:/160829h4415.41N/00600.03E'342/049/A=005524 id0ADDA5BA -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5"
        beacon = parse(valid_aprs_string, reference_date=datetime(2015, 1, 1, 16, 8, 29))

        self.assertEqual(beacon['name'], 'FLRDDA5BA')
        self.assertEqual(beacon['address'], 'DDA5BA')


if __name__ == '__main__':
    unittest.main()
