import unittest
from ogn.parser.aprs_comment.inreach_parser import InreachParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = InreachParser().parse_position("id300434060496190 inReac True")
        assert message['address'] == "300434060496190"
        assert message['model'] == 'inReac'
        assert message['status'] is True
        assert message['pilot_name'] is None

        message = InreachParser().parse_position("id300434060496190 inReac True Jim Bob")
        assert message['address'] == "300434060496190"
        assert message['model'] == 'inReac'
        assert message['status'] is True
        assert message['pilot_name'] == "Jim Bob"


if __name__ == '__main__':
    unittest.main()
