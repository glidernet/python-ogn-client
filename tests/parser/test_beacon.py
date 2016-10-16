import unittest

from datetime import datetime

from ogn.parser.utils import kts2kmh, m2feet
from ogn.parser.parse import parse_aprs
from ogn.parser.exceptions import AprsParseError


class TestStringMethods(unittest.TestCase):
    def test_fail_validation(self):
        with self.assertRaises(AprsParseError):
            parse_aprs("notAValidString")

    def test_basic(self):
        message = parse_aprs("FLRDDA5BA>APRS,qAS,LFMX:/160829h4415.41N/00600.03E'342/049/A=005524 this is a comment",
                             reference_date=datetime(2015, 1, 1, 16, 8, 29))
        self.assertEqual(message['name'], "FLRDDA5BA")
        self.assertEqual(message['receiver_name'], "LFMX")
        self.assertEqual(message['timestamp'].strftime('%H:%M:%S'), "16:08:29")
        self.assertAlmostEqual(message['latitude'], 44.25683, 5)
        self.assertEqual(message['symboltable'], '/')
        self.assertAlmostEqual(message['longitude'], 6.0005, 5)
        self.assertEqual(message['symbolcode'], '\'')
        self.assertEqual(message['track'], 342)
        self.assertEqual(message['ground_speed'], 49 * kts2kmh)
        self.assertAlmostEqual(message['altitude'] * m2feet, 5524, 5)
        self.assertEqual(message['comment'], "this is a comment")

    def test_v024(self):
        # higher precision datum format introduced
        raw_message = "FLRDDA5BA>APRS,qAS,LFMX:/160829h4415.41N/00600.03E'342/049/A=005524 !W26! id21400EA9 -2454fpm +0.9rot 19.5dB 0e -6.6kHz gps1x1 s6.02 h44 rDF0C56"
        message = parse_aprs(raw_message, reference_date=datetime(2015, 1, 1, 16, 8, 29))

        self.assertAlmostEqual(message['latitude'] - 44.2568 - 1 / 30000, 2 / 1000 / 60, 10)
        self.assertAlmostEqual(message['longitude'] - 6.0005, 6 / 1000 / 60, 10)

    def test_v025(self):
        # introduced the "aprs status" format where many informations (lat, lon, alt, speed, ...) are just optional
        raw_message = "EPZR>APRS,TCPIP*,qAC,GLIDERN1:>093456h this is a comment"
        message = parse_aprs(raw_message, reference_date=datetime(2015, 1, 1, 9, 35, 29))

        self.assertEqual(message['name'], "EPZR")
        self.assertEqual(message['receiver_name'], "GLIDERN1")
        self.assertEqual(message['timestamp'].strftime('%H:%M:%S'), "09:34:56")
        self.assertEqual(message['comment'], "this is a comment")

if __name__ == '__main__':
    unittest.main()
