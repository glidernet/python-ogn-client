from ogn.parser.pattern import PATTERN_NAVITER_POSITION_COMMENT
from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS

from .base import BaseParser


class NaviterParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'naviter'
        self.position_pattern = PATTERN_NAVITER_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)
        return {'stealth': (int(match.group('details'), 16) & 0b1000000000000000) >> 15 == 1,
                'do_not_track': (int(match.group('details'), 16) & 0b0100000000000000) >> 14 == 1,
                'aircraft_type': (int(match.group('details'), 16) & 0b0011110000000000) >> 10,
                'address_type': (int(match.group('details'), 16) & 0b0000001111110000) >> 4,
                'reserved': (int(match.group('details'), 16) & 0b0000000000001111),
                'address': match.group('address'),
                'climb_rate': int(match.group('climb_rate')) * FPM_TO_MS if match.group('climb_rate') else None,
                'turn_rate': float(match.group('turn_rate')) * HPM_TO_DEGS if match.group('turn_rate') else None}
