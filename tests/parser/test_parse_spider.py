import unittest

from ogn.parser.aprs_comment.spider_parser import SpiderParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = SpiderParser.parse_position("id300234010617040 +19dB LWE 3D")

        self.assertEqual(message['id'], "300234010617040")
        self.assertEqual(message['signal_strength'], 19)
        self.assertEqual(message['spider_id'], "LWE")
        self.assertEqual(message['gps_status'], "3D")


if __name__ == '__main__':
    unittest.main()
