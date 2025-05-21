import unittest.mock as mock
import pytest

from datetime import datetime

from ogn.parser.telnet_parser import parse
from ogn.parser.exceptions import AprsParseError


@pytest.mark.skip("Not yet implemented")
def test_telnet_fail_corrupt():
    with pytest.raises(AprsParseError):
        parse('This is rubbish')


@mock.patch('ogn.parser.telnet_parser.datetime')
def test_telnet_parse_complete(datetime_mock):
    # set the now-mock near to the time in the test string
    datetime_mock.now.return_value = datetime(2015, 1, 1, 10, 0, 55)

    message = parse('0.181sec:868.394MHz:   1:2:DDA411 103010: [ +50.86800, +12.15279]deg  988m  +0.1m/s  25.7m/s 085.4deg  -3.5deg/sec 5 03x04m 01f_-12.61kHz  5.8/15.5dB/2 10e   30.9km 099.5deg  +1.1deg + ?     R     B8949')

    assert message['pps_offset'] == 0.181
    assert message['frequency'] == 868.394
    assert message['aircraft_type'] == 1
    assert message['address_type'] == 2
    assert message['address'] == 'DDA411'
    assert message['timestamp'] == datetime(2015, 1, 1, 10, 30, 10)
    assert message['latitude'] == 50.868
    assert message['longitude'] == 12.15279
    assert message['altitude'] == 988
    assert message['climb_rate'] == 0.1
    assert message['ground_speed'] == 25.7
    assert message['track'] == 85.4
    assert message['turn_rate'] == -3.5
    assert message['magic_number'] == 5  # the '5' is a magic number... 1 if ground_speed is 0.0m/s an 3 or 5 if airborne. Do you have an idea what it is?
    assert message['gps_status'] == '03x04'
    assert message['channel'] == 1
    assert message['flarm_timeslot'] is True
    assert message['ogn_timeslot'] is False
    assert message['frequency_offset'] == -12.61
    assert message['decode_quality'] == 5.8
    assert message['signal_quality'] == 15.5
    assert message['demodulator_type'] == 2
    assert message['error_count'] == 10
    assert message['distance'] == 30.9
    assert message['bearing'] == 99.5
    assert message['phi'] == 1.1
    assert message['multichannel'] is True


def test_telnet_parse_corrupt():
    message = parse('0.397sec:868.407MHz:  sA:1:784024 205656: [  +5.71003, +20.48951]deg 34012m +14.5m/s 109.7m/s 118.5deg +21.0deg/sec 0 27x40m 01_o +7.03kHz 17.2/27.0dB/2 12e 4719.5km 271.1deg  -8.5deg   ?     R     B34067')

    assert message is None
