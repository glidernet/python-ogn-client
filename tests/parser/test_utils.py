import unittest
from datetime import datetime, timezone

from ogn.parser.utils import parseAngle, createTimestamp, CheapRuler, normalized_quality


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

    def test_createTimestamp_tzinfo(self):
        test_data = [
            ('000001h', datetime(2020, 9, 10, 0, 0, 1, tzinfo=timezone.utc), (datetime(2020, 9, 10, 0, 0, 1, tzinfo=timezone.utc)))
        ]

        self.proceed_test_data(test_data)

    def test_cheap_ruler_distance(self):
        koenigsdf = (11.465353, 47.829825)
        hochkoenig = (13.062405, 47.420516)

        cheap_ruler = CheapRuler((koenigsdf[1] + hochkoenig[1]) / 2)
        distance = cheap_ruler.distance(koenigsdf, hochkoenig)
        self.assertAlmostEqual(distance, 128381.47612138899)

    def test_cheap_ruler_bearing(self):
        koenigsdf = (11.465353, 47.829825)
        hochkoenig = (13.062405, 47.420516)

        cheap_ruler = CheapRuler((koenigsdf[1] + hochkoenig[1]) / 2)
        bearing = cheap_ruler.bearing(koenigsdf, hochkoenig)
        self.assertAlmostEqual(bearing, 110.761300063515)

    def test_normalized_quality(self):
        self.assertAlmostEqual(normalized_quality(10000, 1), 1)
        self.assertAlmostEqual(normalized_quality(20000, 10), 16.020599913279625)
        self.assertAlmostEqual(normalized_quality(5000, 5), -1.0205999132796242)


if __name__ == '__main__':
    unittest.main()
