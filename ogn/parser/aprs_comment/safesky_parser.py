from ogn.parser.utils import FPM_TO_MS
from ogn.parser.pattern import PATTERN_SAFESKY_POSITION_COMMENT

from .base import BaseParser


class SafeskyParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'safesky'
        self.position_pattern = PATTERN_SAFESKY_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)
        result = dict()
        if match.group('details'):
            result.update({
                'address_type': int(match.group('details'), 16) & 0b00000011,
                'aircraft_type': (int(match.group('details'), 16) & 0b00111100) >> 2,
                'no-tracking': (int(match.group('details'), 16) & 0b01000000) >> 6 == 1,
                'stealth': (int(match.group('details'), 16) & 0b10000000) >> 7 == 1,
                'address': match.group('address'),
            })
        result.update(
            {'climb_rate': int(match.group('climb_rate')) * FPM_TO_MS if match.group('climb_rate') else None})
        if match.group('gps_quality'):
            result.update({
                'gps_quality': {
                    'horizontal': int(match.group('gps_quality_horizontal')),
                    'vertical': int(match.group('gps_quality_vertical'))
                }
            })
        return result
