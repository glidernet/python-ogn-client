import unittest
from datetime import date, time, datetime

from ogn.parser.utils import parseAngle, createTimestamp
from ogn.parser.exceptions import AmbigousTimeError


class TestStringMethods(unittest.TestCase):
    def test_parseAngle(self):
        self.assertAlmostEqual(parseAngle('05048.30'), 50.805, 5)

    def proceed_test_data(self, test_data={}):
        for test in test_data:
            if test[3]:
                timestamp = createTimestamp(test[0], reference_date=test[1], reference_time=test[2])
                self.assertEqual(timestamp, test[3])
            else:
                with self.assertRaises(AmbigousTimeError):
                    createTimestamp(test[0], reference_date=test[1], reference_time=test[2])

    def test_createTimestamp_hhmmss(self):
        test_data = [
            ('000001h', date(2015, 1, 10), time(0, 0, 1), datetime(2015, 1, 10, 0, 0, 1)),      # packet from current day (on the tick)
            ('235959h', date(2015, 1, 10), time(0, 0, 1), datetime(2015, 1, 9, 23, 59, 59)),    # packet from previous day (2 seconds old)
            ('110000h', date(2015, 1, 10), time(0, 0, 1), None),                                # packet 11 hours from future or 13 hours old
            ('123500h', date(2015, 1, 10), time(23, 50, 0), datetime(2015, 1, 10, 12, 35, 0)),   # packet from current day (11 hours old)
            ('000001h', date(2015, 1, 10), time(23, 50, 0), datetime(2015, 1, 11, 0, 0, 1)),     # packet from next day (11 minutes from future)
            ('000001h', date(2015, 1, 10), None, datetime(2015, 1, 10, 0, 0, 1)),                # first packet of a specific day
            ('235959h', date(2015, 1, 10), None, datetime(2015, 1, 10, 23, 59, 59)),             # last packet of a specific day
        ]

        self.proceed_test_data(test_data)

    def test_createTimestamp_ddhhmm(self):
        test_data = [
            ('011212z', date(2017, 9, 28), time(0, 0, 1), datetime(2017, 9, 1, 12, 12, 0)),      # packet from 1st of month, received on september 28th,
            ('281313z', date(2017, 10, 1), time(0, 0, 1), datetime(2017, 9, 28, 13, 13, 0)),     # packet from 28th of month, received on october 1st,
            ('281414z', date(2017, 1, 1), time(0, 0, 1), datetime(2016, 12, 28, 14, 14, 0)),     # packet from 28th of month, received on january 1st,
        ]

        self.proceed_test_data(test_data)


if __name__ == '__main__':
    unittest.main()
