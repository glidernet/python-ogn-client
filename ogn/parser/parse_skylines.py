import re

from ogn.parser.utils import fpm2ms
from ogn.parser.pattern import PATTERN_AIRCRAFT_BEACON
from ogn.parser.exceptions import OgnParseError


def parse(aprs_comment):
    ac_match = re.search(PATTERN_AIRCRAFT_BEACON, aprs_comment)
    if ac_match:
        return {'address': ac_match.group('deviceID'), 'climb_rate': int(ac_match.group('climb_rate')) * fpm2ms if ac_match.group('climb_rate') else None}
    else:
        raise OgnParseError("Parser error ... wrong format")
