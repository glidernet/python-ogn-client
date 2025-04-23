import pytest

from ogn.parser.utils import FPM_TO_MS
from ogn.parser.aprs_comment.fanet_parser import FanetParser


def test_position_comment():
    message = FanetParser().parse_position("id1E1103CE -02fpm")

    assert message['address_type'] == 2
    assert message['aircraft_type'] == 7
    assert message['stealth'] is False
    assert message['address'] == "1103CE"
    assert message['climb_rate'] == pytest.approx(-2 * FPM_TO_MS, 0.1)


def test_pseudo_status_comment():
    message = FanetParser().parse_position("")

    assert message == {}


def test_v028_status():
    message = FanetParser().parse_status('Name="Juerg Zweifel" 15.0dB -17.1kHz 1e')

    assert message['fanet_name'] == "Juerg Zweifel"
    assert message['signal_quality'] == 15.0
    assert message['frequency_offset'] == -17.1
    assert message['error_count'] == 1
