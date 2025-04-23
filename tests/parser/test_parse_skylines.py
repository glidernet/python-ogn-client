import pytest

from ogn.parser.utils import FPM_TO_MS
from ogn.parser.aprs_comment.skylines_parser import SkylinesParser


def test_position_comment():
    message = SkylinesParser().parse_position("id2816 -015fpm")

    assert message['skylines_id'] == "2816"
    assert message['climb_rate'] == pytest.approx(-15 * FPM_TO_MS, 2)
