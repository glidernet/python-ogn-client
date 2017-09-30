import re

from ogn.parser.utils import fpm2ms
from ogn.parser.pattern import PATTERN_NAVITER_BEACON


def parse(aprs_comment):
    match = re.search(PATTERN_NAVITER_BEACON, aprs_comment)
    return {'stealth': (int(match.group('details'), 16) & 0b1000000000000000) >> 15 == 1,
            'do_not_track': (int(match.group('details'), 16) & 0b0100000000000000) >> 14 == 1,
            'aircraft_type': (int(match.group('details'), 16) & 0b0011110000000000) >> 10,
            'address_type': (int(match.group('details'), 16) & 0b0000001111110000) >> 4,
            'reserved': (int(match.group('details'), 16) & 0b0000000000001111),
            'address': match.group('id'),
            'climb_rate': int(match.group('climb_rate')) * fpm2ms if match.group('climb_rate') else None,
            'turn_rate': float(match.group('turn_rate')) if match.group('turn_rate') else None}
