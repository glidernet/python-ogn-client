from ogn.parser.utils import FPM_TO_MS
from ogn.parser.pattern import PATTERN_FANET_POSITION_COMMENT

from .base import BaseParser


class FanetParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'fanet'
        self.position_parser = PATTERN_FANET_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_parser.match(aprs_comment)
        result = {}
        if match.group('details'):
            result.update({
                'address_type': int(match.group('details'), 16) & 0b00000011,
                'aircraft_type': (int(match.group('details'), 16) & 0b01111100) >> 2,
                'stealth': (int(match.group('details'), 16) & 0b10000000) >> 7 == 1,
                'address': match.group('address')
            })
        if match.group('climb_rate'): result['climb_rate'] = int(match.group('climb_rate')) * FPM_TO_MS
        return result
