import unittest

from ogn.parser.aprs_comment.spider_parser import SpiderParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = SpiderParser().parse_position("id300234060668560 +30dB K23W 3D")

        self.assertEqual(message['spider_id'], "300234060668560")
        self.assertEqual(message['signal_power'], 30)
        self.assertEqual(message['spider_registration'], "K23W")
        self.assertEqual(message['gps_quality'], "3D")


if __name__ == '__main__':
    unittest.main()
