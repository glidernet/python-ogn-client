import unittest

from ogn.parser.utils import FPM_TO_MS
from ogn.parser.aprs_comment.safesky_parser import SafeskyParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        # "SKY3E5906>OGNSKY,qAS,SafeSky:/072555h5103.47N/00524.81E'065/031/A=001250 !W05! id1C3E5906 +010fpm gps6x1"
        message = SafeskyParser().parse_position("id1C3E5906 +010fpm gps6x1")
        self.assertEqual(message['address'], '3E5906')
        self.assertEqual(message['address_type'], 0)
        self.assertEqual(message['aircraft_type'], 7)
        self.assertFalse(message['stealth'])
        self.assertAlmostEqual(message['climb_rate'], 10 * FPM_TO_MS, 2)
        self.assertEqual(message['gps_quality'], {'horizontal': 6, 'vertical': 1})


if __name__ == '__main__':
    unittest.main()
