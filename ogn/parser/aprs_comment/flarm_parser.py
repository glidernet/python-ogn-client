from ogn.parser.pattern import PATTERN_FLARM_POSITION_COMMENT
from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS

from .base import BaseParser


class FlarmParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'flarm'
        self.position_pattern = PATTERN_FLARM_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)

        result = {}
        if match.group('details'):
            result.update({
                'address_type': int(match.group('details'), 16) & 0b00000011,
                'aircraft_type': (int(match.group('details'), 16) & 0b01111100) >> 2,
                'stealth': (int(match.group('details'), 16) & 0b10000000) >> 7 == 1,
                'address': match.group('address'),
            })
        if match.group('climb_rate'): result['climb_rate'] = int(match.group('climb_rate')) * FPM_TO_MS
        if match.group('turn_rate'): result['turn_rate'] = float(match.group('turn_rate')) * HPM_TO_DEGS
        if match.group('signal_quality'): result['signal_quality'] = float(match.group('signal_quality'))
        if match.group('error_count'): result['error_count'] = int(match.group('error_count'))
        if match.group('frequency_offset'): result['frequency_offset'] = float(match.group('frequency_offset'))
        if match.group('gps_quality'):
            result.update({
                'gps_quality': {
                    'horizontal': int(match.group('gps_quality_horizontal')),
                    'vertical': int(match.group('gps_quality_vertical'))
                }
            })
        if match.group('software_version'): result['software_version'] = float(match.group('software_version'))
        if match.group('hardware_version'): result['hardware_version'] = int(match.group('hardware_version'), 16)
        if match.group('real_address'): result['real_address'] = match.group('real_address')
        if match.group('signal_power'): result['signal_power'] = float(match.group('signal_power'))
        return result
