import unittest
from datetime import date, time, datetime

from ogn.parser.utils import parseAngle, createTimestamp
from ogn.parser.exceptions import AmbigousTimeError


class TestStringMethods(unittest.TestCase):
    def test_parseAngle(self):
        self.assertAlmostEqual(parseAngle('05048.30'), 50.805, 5)

    def test_createTimestamp(self):
        test_data = [
            ('000001', date(2015, 1, 10), time(0, 0, 1), datetime(2015, 1, 10, 0, 0, 1)),      # packet from current day (on the tick)
            ('235959', date(2015, 1, 10), time(0, 0, 1), datetime(2015, 1, 9, 23, 59, 59)),    # packet from previous day (2 seconds old)
            ('110000', date(2015, 1, 10), time(0, 0, 1), None),                                # packet 11 hours from future or 13 hours old
            ('123500', date(2015, 1, 10), time(23, 50, 0), datetime(2015, 1, 10, 12, 35, 0)),   # packet from current day (11 hours old)
            ('000001', date(2015, 1, 10), time(23, 50, 0), datetime(2015, 1, 11, 0, 0, 1)),     # packet from next day (11 minutes from future)
            ('000001', date(2015, 1, 10), None, datetime(2015, 1, 10, 0, 0, 1)),                # first packet of a specific day
            ('235959', date(2015, 1, 10), None, datetime(2015, 1, 10, 23, 59, 59)),             # last packet of a specific day
        ]

        for test in test_data:
            if test[3]:
                timestamp = createTimestamp(test[0], reference_date=test[1], reference_time=test[2])
                self.assertEqual(timestamp, test[3])
            else:
                with self.assertRaises(AmbigousTimeError):
                    createTimestamp(test[0], reference_date=test[1], reference_time=test[2])

if __name__ == '__main__':
    unittest.main()
