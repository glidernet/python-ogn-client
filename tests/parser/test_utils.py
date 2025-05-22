import pytest
from datetime import datetime, timezone

from ogn.parser.utils import parseAngle, createTimestamp, CheapRuler, normalized_quality


def _proceed_test_data(test_data={}):
    for test in test_data:
        timestamp = createTimestamp(test[0], reference_timestamp=test[1])
        assert timestamp == test[2]


def test_parseAngle():
    assert parseAngle('05048.30') == 50.805


def test_createTimestamp_hhmmss():
    test_data = [
        ('000001h', datetime(2015, 1, 10, 0, 0, 1), datetime(2015, 1, 10, 0, 0, 1)),        # packet from current day (on the tick)
        ('235959h', datetime(2015, 1, 10, 0, 0, 1), datetime(2015, 1, 9, 23, 59, 59)),      # packet from previous day (2 seconds old)
        ('110000h', datetime(2015, 1, 10, 0, 0, 1), datetime(2015, 1, 10, 11, 0, 0)),       # packet 11 hours from future or 13 hours old
        ('123500h', datetime(2015, 1, 10, 23, 50, 0), datetime(2015, 1, 10, 12, 35, 0)),    # packet from current day (11 hours old)
        ('000001h', datetime(2015, 1, 10, 23, 50, 0), datetime(2015, 1, 11, 0, 0, 1)),      # packet from next day (11 minutes from future)
    ]

    _proceed_test_data(test_data)


def test_createTimestamp_ddhhmm():
    test_data = [
        ('011212z', datetime(2017, 9, 28, 0, 0, 1), datetime(2017, 10, 1, 12, 12, 0)),      # packet from 1st of month, received on september 28th,
        ('281313z', datetime(2017, 10, 1, 0, 0, 1), datetime(2017, 9, 28, 13, 13, 0)),      # packet from 28th of month, received on october 1st,
        ('281414z', datetime(2017, 1, 1, 0, 0, 1), datetime(2016, 12, 28, 14, 14, 0)),      # packet from 28th of month, received on january 1st,
    ]

    _proceed_test_data(test_data)


def test_createTimestamp_tzinfo():
    test_data = [
        ('000001h', datetime(2020, 9, 10, 0, 0, 1, tzinfo=timezone.utc), (datetime(2020, 9, 10, 0, 0, 1, tzinfo=timezone.utc)))
    ]

    _proceed_test_data(test_data)


def test_cheap_ruler_distance():
    koenigsdf = (11.465353, 47.829825)
    hochkoenig = (13.062405, 47.420516)

    cheap_ruler = CheapRuler((koenigsdf[1] + hochkoenig[1]) / 2)
    distance = cheap_ruler.distance(koenigsdf, hochkoenig)
    assert distance == pytest.approx(128381.47612138899)


def test_cheap_ruler_bearing():
    koenigsdf = (11.465353, 47.829825)
    hochkoenig = (13.062405, 47.420516)

    cheap_ruler = CheapRuler((koenigsdf[1] + hochkoenig[1]) / 2)
    bearing = cheap_ruler.bearing(koenigsdf, hochkoenig)
    assert bearing == pytest.approx(110.761300063515)


def test_normalized_quality():
    assert normalized_quality(10000, 1) == pytest.approx(1)
    assert normalized_quality(20000, 10) == pytest.approx(16.020599913279625)
    assert normalized_quality(5000, 5) == pytest.approx(-1.0205999132796242)
