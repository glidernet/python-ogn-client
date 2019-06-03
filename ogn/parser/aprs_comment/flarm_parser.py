import re

from ogn.parser.pattern import PATTERN_FLARM_POSITION_COMMENT
from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS

from .base import BaseParser


class FlarmParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'flarm'
        self.position_pattern = re.compile(PATTERN_FLARM_POSITION_COMMENT)

    def parse_position(self, aprs_comment):
        ac_match = self.position_pattern.match(aprs_comment)
        return {'address_type': int(ac_match.group('details'), 16) & 0b00000011,
                'aircraft_type': (int(ac_match.group('details'), 16) & 0b01111100) >> 2,
                'stealth': (int(ac_match.group('details'), 16) & 0b10000000) >> 7 == 1,
                'address': ac_match.group('address'),
                'climb_rate': int(ac_match.group('climb_rate')) * FPM_TO_MS,
                'turn_rate': float(ac_match.group('turn_rate')) * HPM_TO_DEGS,
                'signal_quality': float(ac_match.group('signal_quality')),
                'error_count': int(ac_match.group('error_count')),
                'frequency_offset': float(ac_match.group('frequency_offset')),
                'gps_quality': {'horizontal': int(ac_match.group('gps_quality_horizontal')),
                                'vertical': int(ac_match.group('gps_quality_vertical'))} if ac_match.group('gps_quality') else None,
                'software_version': float(ac_match.group('software_version')) if ac_match.group('software_version') else None,
                'hardware_version': int(ac_match.group('hardware_version'), 16) if ac_match.group('hardware_version') else None,
                'real_address': ac_match.group('real_address') if ac_match.group('real_address') else None,
                'signal_power': float(ac_match.group('signal_power')) if ac_match.group('signal_power') else None}
