import unittest

from ogn.parser.aprs_comment.spot_parser import SpotParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = SpotParser().parse_position("id0-2860357 SPOT3 GOOD")

        assert message['spot_id'] == "0-2860357"
        assert message['model'] == 'SPOT3'
        assert message['status'] == "GOOD"


if __name__ == '__main__':
    unittest.main()
