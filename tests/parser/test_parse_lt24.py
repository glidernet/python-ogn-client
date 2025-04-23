import pytest

from ogn.parser.utils import FPM_TO_MS
from ogn.parser.aprs_comment.lt24_parser import LT24Parser


def test_position_comment():
    message = LT24Parser().parse_position("id25387 +123fpm GPS")

    assert message['lt24_id'] == "25387"
    assert message['climb_rate'] == pytest.approx(123 * FPM_TO_MS, 2)
    assert message['source'] == 'GPS'
