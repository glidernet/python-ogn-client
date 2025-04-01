from ogn.parser.pattern import PATTERN_MICROTRAK_POSITION_COMMENT

from .base import BaseParser


class MicrotrakParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'microtrak'
        self.position_pattern = PATTERN_MICROTRAK_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)

        result = {}
        if match.group('details'):
            result.update({
                'address_type': int(match.group('details'), 16) & 0b00000011,
                'aircraft_type': (int(match.group('details'), 16) & 0b00111100) >> 2,
                'no-tracking': (int(match.group('details'), 16) & 0b01000000) >> 6 == 1,
                'stealth': (int(match.group('details'), 16) & 0b10000000) >> 7 == 1,
                'address': match.group('address'),
            })
        return result
