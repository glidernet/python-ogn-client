import pytest

from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS
from ogn.parser.aprs_comment.ogn_parser import OgnParser


def test_invalid_token():
    assert OgnParser().parse_aircraft_beacon("notAValidToken") is None


def test_basic():
    message = OgnParser().parse_aircraft_beacon("id0ADDA5BA -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5 hear1084 hearB597 hearB598")

    assert message['address_type'] == 2
    assert message['aircraft_type'] == 2
    assert message['stealth'] is False
    assert message['no-tracking'] is False
    assert message['address'] == "DDA5BA"
    assert message['climb_rate'] == pytest.approx(-454 * FPM_TO_MS, 2)
    assert message['turn_rate'] == -1.1 * HPM_TO_DEGS
    assert message['signal_quality'] == 8.8
    assert message['error_count'] == 0
    assert message['frequency_offset'] == 51.2
    assert message['gps_quality'] == {'horizontal': 4, 'vertical': 5}
    assert len(message['proximity']) == 3
    assert message['proximity'][0] == '1084'
    assert message['proximity'][1] == 'B597'
    assert message['proximity'][2] == 'B598'


def test_no_tracking():
    message = OgnParser().parse_aircraft_beacon("id0ADD1234 -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5 hear1084 hearB597 hearB598")
    assert message['no-tracking'] is False

    message = OgnParser().parse_aircraft_beacon("id4ADD1234 -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5 hear1084 hearB597 hearB598")
    assert message['no-tracking'] is True


def test_stealth():
    message = OgnParser().parse_aircraft_beacon("id0ADD1234 -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5 hear1084 hearB597 hearB598")
    assert message['stealth'] is False

    message = OgnParser().parse_aircraft_beacon("id8ADD1234 -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5 hear1084 hearB597 hearB598")
    assert message['stealth'] is True


def test_v024():
    message = OgnParser().parse_aircraft_beacon("id21400EA9 -2454fpm +0.9rot 19.5dB 0e -6.6kHz gps1x1 s6.02 h0A rDF0C56")

    assert message['software_version'] == 6.02
    assert message['hardware_version'] == 10
    assert message['real_address'] == "DF0C56"


def test_v024_ogn_tracker():
    message = OgnParser().parse_aircraft_beacon("id07353800 +020fpm -14.0rot FL004.43 38.5dB 0e -2.9kHz")

    assert message['flightlevel'] == 4.43


def test_v025():
    message = OgnParser().parse_aircraft_beacon("id06DDE28D +535fpm +3.8rot 11.5dB 0e -1.0kHz gps2x3 s6.01 h0C +7.4dBm")

    assert message['signal_power'] == 7.4


def test_v026():
    # from 0.2.6 it is sufficent we have only the ID, climb and turn rate or just the ID
    message_triple = OgnParser().parse_aircraft_beacon("id093D0930 +000fpm +0.0rot")
    message_single = OgnParser().parse_aircraft_beacon("id093D0930")

    assert message_triple is not None
    assert message_single is not None


def test_relevant_keys_only():
    # return only keys where we got informations
    message = OgnParser().parse_aircraft_beacon("id093D0930")

    assert message is not None
    assert sorted(message.keys()) == sorted(['address_type', 'aircraft_type', 'stealth', 'address', 'no-tracking'])
