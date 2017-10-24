import re

from ogn.parser.pattern import PATTERN_AIRCRAFT_BEACON
from ogn.parser.exceptions import OgnParseError


def parse(aprs_comment):
    ac_match = re.search(PATTERN_AIRCRAFT_BEACON, aprs_comment)
    if ac_match:
        return {'address': ac_match.group('deviceID')}
    else:
        raise OgnParseError("Parser error ... wrong format")
