import pytest

from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS
from ogn.parser.aprs_comment.flarm_parser import FlarmParser


def test_position_comment():
    message = FlarmParser().parse_position("id21A8CBA8 -039fpm +0.1rot 3.5dB 2e -8.7kHz gps1x2 s6.09 h43 rDF0267")

    assert message['address_type'] == 1
    assert message['aircraft_type'] == 8
    assert message['stealth'] is False
    assert message['no-tracking'] is False
    assert message['address'] == "A8CBA8"
    assert message['climb_rate'] == pytest.approx(-39 * FPM_TO_MS, 2)
    assert message['turn_rate'] == 0.1 * HPM_TO_DEGS
    assert message['signal_quality'] == 3.5
    assert message['error_count'] == 2
    assert message['frequency_offset'] == -8.7
    assert message['gps_quality'] == {'horizontal': 1, 'vertical': 2}
    assert message['software_version'] == 6.09
    assert message['hardware_version'] == 67
    assert message['real_address'] == "DF0267"


def test_position_comment_relevant_keys_only():
    # return only keys where we got informations
    message = FlarmParser().parse_position("id21A8CBA8")

    assert message is not None
    assert sorted(message.keys()) == sorted(['address_type', 'aircraft_type', 'stealth', 'address', 'no-tracking'])
