import unittest

from ogn.parser.aprs_comment.generic_parser import GenericParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = GenericParser().parse_position("id0123456789 weather is good, climbing with 123fpm")
        self.assertTrue('comment' in message)

        message = GenericParser().parse_status("id0123456789 weather is good, climbing with 123fpm")
        self.assertTrue('comment' in message)


if __name__ == '__main__':
    unittest.main()
