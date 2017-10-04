import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.parse_lt24 import OGLT24


class TestStringMethods(unittest.TestCase):
    @unittest.skip("Not yet implemented")
    def test(self):
        message = OGLT24.parse_position("id25387 +000fpm GPS")

        self.assertEqual(message['id'], 25387)
        self.assertAlmostEqual(message['climb_rate'] * ms2fpm, 0, 2)
        self.assertEqual(message['wtf'], 'GPS')


if __name__ == '__main__':
    unittest.main()
