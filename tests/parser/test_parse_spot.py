import unittest

from ogn.parser.aprs_comment.spot_parser import SpotParser


class TestStringMethods(unittest.TestCase):
    def test(self):
        message = SpotParser.parse_position("id0-2860357 SPOT3 GOOD")

        self.assertEqual(message['id'], "0-2860357")
        self.assertEqual(message['model'], 3)
        self.assertEqual(message['status'], "GOOD")


if __name__ == '__main__':
    unittest.main()
