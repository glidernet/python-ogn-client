import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.parse_naviter import parse


class TestStringMethods(unittest.TestCase):
    def test_OGNAVI_1(self):
        message = parse("id0440042121 +123fpm +0.5rot")

        # id0440042121 == 0b0000 0100 0100 0000 0000 0100 0010 0001 0010 0001
        # bit 0: stealth mode
        # bit 1: do not track mode
        # bits 2-5: aircraft type
        # bits 6-11: address type (namespace is extended from 2 to 6 bits to avoid collisions with other tracking providers)
        # bits 12-15: reserved for use at a later time
        # bits 16-39: device id (24-bit device identifier, same as in APRS header)
        self.assertEqual(message['stealth'], False)
        self.assertEqual(message['do_not_track'], False)
        self.assertEqual(message['aircraft_type'], 1)
        self.assertEqual(message['address_type'], 4)
        self.assertEqual(message['reserved'], 0)
        self.assertEqual(message['address'], "042121")

        self.assertAlmostEqual(message['climb_rate'] * ms2fpm, 123, 2)
        self.assertEqual(message['turn_rate'], 0.5)


if __name__ == '__main__':
    unittest.main()
