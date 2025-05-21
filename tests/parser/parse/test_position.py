import pytest

from ogn.parser import parse
from ogn.parser.exceptions import AprsParseError
from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS, KNOTS_TO_MS, KPH_TO_MS, FEETS_TO_METER


def test_basic():
    raw_message = r"FLRDDA5BA>APRS,qAS,LFMX:/160829h4415.41N/00600.03E'342/049/A=005524 this is a comment"
    message = parse(raw_message)

    assert message['aprs_type'] == 'position'
    assert message['beacon_type'] == 'unknown'

    assert message['name'] == "FLRDDA5BA"
    assert message['dstcall'] == "APRS"
    assert message['receiver_name'] == "LFMX"
    assert message['timestamp'].strftime('%H:%M:%S') == "16:08:29"
    assert message['latitude'] == pytest.approx(44.25683, 5)
    assert message['symboltable'] == '/'
    assert message['longitude'] == pytest.approx(6.0005, 5)
    assert message['symbolcode'] == '\''
    assert message['track'] == 342
    assert message['ground_speed'] == 49 * KNOTS_TO_MS / KPH_TO_MS
    assert message['altitude'] == pytest.approx(5524 * FEETS_TO_METER, 5)
    assert message['user_comment'] == "this is a comment"


def test_v026_relay():
    # beacons can be relayed
    raw_message = "FLRFFFFFF>OGNAVI,NAV07220E*,qAS,NAVITER:/092002h1000.00S/01000.00W'000/000/A=003281 !W00! id2820FFFFFF +300fpm +1.7rot"
    message = parse(raw_message)

    assert message['aprs_type'] == 'position'
    assert message['beacon_type'] == 'naviter'

    assert message['relay'] == "NAV07220E"


def test_no_altitude():
    # altitude is not a 'must have'
    raw_message = "FLRDDEEF1>OGCAPT,qAS,CAPTURS:/065511h4837.63N/00233.79E'000/000"
    message = parse(raw_message)

    assert message['aprs_type'] == 'position'
    assert message['beacon_type'] == 'capturs'

    assert message.get('altitude') is None


def test_invalid_coordinates():
    # sometimes the coordinates leave their valid range: -90<=latitude<=90 or -180<=longitude<=180
    with pytest.raises(AprsParseError):
        parse("RND000000>APRS,qAS,TROCALAN1:/210042h6505.31S/18136.75W^054/325/A=002591 !W31! idA4000000 +099fpm +1.8rot FL029.04 12.0dB 5e -6.3kHz gps11x17")

    with pytest.raises(AprsParseError):
        parse("RND000000>APRS,qAS,TROCALAN1:/210042h9505.31S/17136.75W^054/325/A=002591 !W31! idA4000000 +099fpm +1.8rot FL029.04 12.0dB 5e -6.3kHz gps11x17")


def test_invalid_timestamp():
    with pytest.raises(AprsParseError):
        parse("OGND4362A>APRS,qAS,Eternoz:/194490h4700.25N/00601.47E'003/063/A=000000 !W22! id07D4362A 0fpm +0.0rot FL000.00 2.0dB 3e -2.8kHz gps3x4 +12.2dBm")

    with pytest.raises(AprsParseError):
        parse("Ulrichamn>APRS,TCPIP*,qAC,GLIDERN1:/194490h5747.30NI01324.77E&/A=001322")


def test():
    raw_message = r"FLRDDEEF1>OGCAPT,qAS,CAPTURS:/065511h4837.63N/00233.79E'255/045/A=003399 !W03! id06DDFAA3 -613fpm -3.9rot 22.5dB 7e -7.0kHz gps3x7 s7.07 h41 rD002F8"
    message = parse(raw_message)

    assert message['aprs_type'] == 'position'
    assert message['beacon_type'] == 'capturs'

    assert message['name'] == "FLRDDEEF1"
    assert message['dstcall'] == "OGCAPT"
    assert message['receiver_name'] == "CAPTURS"
    assert message['timestamp'].strftime('%H:%M:%S') == "06:55:11"
    assert message['latitude'] == pytest.approx(48.62605, 5)
    assert message['longitude'] == pytest.approx(2.56298, 5)
    assert message['symboltable'] == '/'
    assert message['symbolcode'] == '\''
    assert message['track'] == 255
    assert message['ground_speed'] == 45 * KNOTS_TO_MS / KPH_TO_MS
    assert message['altitude'] == pytest.approx(3399 * FEETS_TO_METER, 5)

    assert message['address_type'] == 2
    assert message['aircraft_type'] == 1
    assert message['stealth'] is False
    assert message['no-tracking'] is False
    assert message['address'] == 'DDFAA3'
    assert message['climb_rate'] == pytest.approx(-613 * FPM_TO_MS, 0.1)
    assert message['turn_rate'] == pytest.approx(-3.9 * HPM_TO_DEGS, 0.1)
    assert message['signal_quality'] == 22.5
    assert message['error_count'] == 7
    assert message['frequency_offset'] == -7.0
    assert message['gps_quality'] == '3x7'
    assert message['software_version'] == 7.07
    assert message['hardware_version'] == 65
    assert message['real_address'] == 'D002F8'
