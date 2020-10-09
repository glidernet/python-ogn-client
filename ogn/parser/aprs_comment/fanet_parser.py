from ogn.parser.utils import FPM_TO_MS
from ogn.parser.pattern import PATTERN_FANET_POSITION_COMMENT, PATTERN_FANET_STATUS_COMMENT

from .base import BaseParser


class FanetParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'fanet'
        self.position_pattern = PATTERN_FANET_POSITION_COMMENT
        self.status_pattern = PATTERN_FANET_STATUS_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)
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

    def parse_status(self, aprs_comment):
        match = self.status_pattern.match(aprs_comment)
        result = {}
        if match.group('fanet_name'): result['fanet_name'] = match.group('fanet_name')
        if match.group('signal_quality'): result['signal_quality'] = float(match.group('signal_quality'))
        if match.group('frequency_offset'): result['frequency_offset'] = float(match.group('frequency_offset'))
        if match.group('error_count'): result['error_count'] = int(match.group('error_count'))

        return result
