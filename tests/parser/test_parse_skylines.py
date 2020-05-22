import unittest

from ogn.parser.utils import FPM_TO_MS
from ogn.parser.aprs_comment.skylines_parser import SkylinesParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = SkylinesParser().parse_position("id2816 -015fpm")

        self.assertEqual(message['skylines_id'], "2816")
        self.assertAlmostEqual(message['climb_rate'], -15 * FPM_TO_MS, 2)


if __name__ == '__main__':
    unittest.main()
