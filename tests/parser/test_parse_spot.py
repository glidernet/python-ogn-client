import unittest

from ogn.parser.aprs_comment.spot_parser import SpotParser


class TestStringMethods(unittest.TestCase):
    @unittest.skip("Not yet implemented")
    def test(self):
        message = SpotParser.parse_position("id0-2860357 SPOT3 GOOD")

        self.assertEqual(message['id'], "0-2860357")
        self.assertEqual(message['hw_version'], 3)
        self.assertEqual(message['wtf'], "GOOD")


if __name__ == '__main__':
    unittest.main()
