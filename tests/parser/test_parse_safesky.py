import pytest

from ogn.parser.utils import FPM_TO_MS
from ogn.parser.aprs_comment.safesky_parser import SafeskyParser


def test_position_comment():
    # "SKY3E5906>OGNSKY,qAS,SafeSky:/072555h5103.47N/00524.81E'065/031/A=001250 !W05! id1C3E5906 +010fpm gps6x1"
    message = SafeskyParser().parse_position("id1C3E5906 +010fpm gps6x1")
    assert message['address'] == '3E5906'
    assert message['address_type'] == 0
    assert message['aircraft_type'] == 7
    assert message['stealth'] is False
    assert message['climb_rate'] == pytest.approx(10 * FPM_TO_MS, 2)
    assert message['gps_quality'] == {'horizontal': 6, 'vertical': 1}
