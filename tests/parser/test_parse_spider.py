import unittest

from ogn.parser.aprs_comment.spider_parser import SpiderParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = SpiderParser.parse_position("id300234010617040 +19dB LWE 3D")

        self.assertEqual(message['address'], "300234010617040")
        self.assertEqual(message['signal_power'], 19)
        self.assertEqual(message['spider_id'], "LWE")
        self.assertEqual(message['gps_quality'], "3D")


if __name__ == '__main__':
    unittest.main()
