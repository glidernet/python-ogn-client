import unittest

from ogn.parser.aprs_comment.microtrak_parser import MicrotrakParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = MicrotrakParser().parse_position("id21A8CBA8")

        self.assertEqual(message['address_type'], 1)
        self.assertEqual(message['aircraft_type'], 8)
        self.assertFalse(message['stealth'])
        self.assertFalse(message['no-tracking'])
        self.assertEqual(message['address'], "A8CBA8")

    def test_position_comment_relevant_keys_only(self):
        # return only keys where we got informations
        message = MicrotrakParser().parse_position("id21A8CBA8")

        self.assertIsNotNone(message)
        self.assertEqual(sorted(message.keys()), sorted(['address_type', 'aircraft_type', 'stealth', 'address', 'no-tracking']))


if __name__ == '__main__':
    unittest.main()
