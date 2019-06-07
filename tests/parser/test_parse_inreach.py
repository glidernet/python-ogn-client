import unittest
from ogn.parser.aprs_comment.inreach_parser import InreachParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = InreachParser().parse_position("id300434060496190 inReac True")
        self.assertEqual(message['address'], "300434060496190")
        self.assertEqual(message['model'], 'inReac')
        self.assertEqual(message['status'], True)
        self.assertEqual(message['pilot_name'], None)

        message = InreachParser().parse_position("id300434060496190 inReac True Jim Bob")
        self.assertEqual(message['address'], "300434060496190")
        self.assertEqual(message['model'], 'inReac')
        self.assertEqual(message['status'], True)
        self.assertEqual(message['pilot_name'], "Jim Bob")


if __name__ == '__main__':
    unittest.main()
