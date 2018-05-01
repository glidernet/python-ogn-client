import unittest
from datetime import datetime

from ogn.parser.utils import parseAngle, createTimestamp


class TestStringMethods(unittest.TestCase):
    def test_parseAngle(self):
        self.assertAlmostEqual(parseAngle('05048.30'), 50.805, 5)

    def proceed_test_data(self, test_data={}):
        for test in test_data:
            timestamp = createTimestamp(test[0], reference_timestamp=test[1])
            self.assertEqual(timestamp, test[2])

    def test_createTimestamp_hhmmss(self):
        test_data = [
            ('000001h', datetime(2015, 1, 10, 0, 0, 1), datetime(2015, 1, 10, 0, 0, 1)),        # packet from current day (on the tick)
            ('235959h', datetime(2015, 1, 10, 0, 0, 1), datetime(2015, 1, 9, 23, 59, 59)),      # packet from previous day (2 seconds old)
            ('110000h', datetime(2015, 1, 10, 0, 0, 1), datetime(2015, 1, 10, 11, 0, 0)),       # packet 11 hours from future or 13 hours old
            ('123500h', datetime(2015, 1, 10, 23, 50, 0), datetime(2015, 1, 10, 12, 35, 0)),    # packet from current day (11 hours old)
            ('000001h', datetime(2015, 1, 10, 23, 50, 0), datetime(2015, 1, 11, 0, 0, 1)),      # packet from next day (11 minutes from future)
        ]

        self.proceed_test_data(test_data)

    def test_createTimestamp_ddhhmm(self):
        test_data = [
            ('011212z', datetime(2017, 9, 28, 0, 0, 1), datetime(2017, 10, 1, 12, 12, 0)),      # packet from 1st of month, received on september 28th,
            ('281313z', datetime(2017, 10, 1, 0, 0, 1), datetime(2017, 9, 28, 13, 13, 0)),      # packet from 28th of month, received on october 1st,
            ('281414z', datetime(2017, 1, 1, 0, 0, 1), datetime(2016, 12, 28, 14, 14, 0)),      # packet from 28th of month, received on january 1st,
        ]

        self.proceed_test_data(test_data)


if __name__ == '__main__':
    unittest.main()
