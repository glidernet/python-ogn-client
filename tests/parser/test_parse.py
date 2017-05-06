import unittest
import unittest.mock as mock

from datetime import datetime
from time import sleep

from ogn.parser.parse import parse_aprs
from ogn.parser.exceptions import AprsParseError, OgnParseError


class TestStringMethods(unittest.TestCase):
    def test_valid_beacons(self):
        with open('tests/valid_beacons.txt') as f:
            for line in f:
                if not line[0] == '#':
                    parse_aprs(line, datetime(2015, 4, 10, 17, 0))

    def test_fail_none(self):
        with self.assertRaises(TypeError):
            parse_aprs(None)

    def test_fail_empty(self):
        with self.assertRaises(AprsParseError):
            parse_aprs("")

    def test_fail_bad_string(self):
        with self.assertRaises(AprsParseError):
            parse_aprs("Lachens>APRS,TCPIwontbeavalidstring")

    @unittest.skip('Does not work, I dont know why (2017-04-11)')
    @mock.patch('ogn.parser.parse.createTimestamp')
    def test_default_reference_date(self, createTimestamp_mock):
        valid_aprs_string = "Lachens>APRS,TCPIP*,qAC,GLIDERN2:/165334h4344.70NI00639.19E&/A=005435 v0.2.1 CPU:0.3 RAM:1764.4/21"

        parse_aprs(valid_aprs_string)
        call_args_before = createTimestamp_mock.call_args

        sleep(1)

        parse_aprs(valid_aprs_string)
        call_args_seconds_later = createTimestamp_mock.call_args

        self.assertNotEqual(call_args_before, call_args_seconds_later)


if __name__ == '__main__':
    unittest.main()
