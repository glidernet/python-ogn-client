from ogn.parser.pattern import PATTERN_FLARM_POSITION_COMMENT
from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS

from .base import BaseParser


class FlarmParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'flarm'
        self.position_pattern = PATTERN_FLARM_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)

        return {k: v for (k, v) in
                {'address_type': int(match.group('details'), 16) & 0b00000011 if match.group('details') else None,
                 'aircraft_type': (int(match.group('details'), 16) & 0b01111100) >> 2 if match.group('details') else None,
                 'stealth': (int(match.group('details'), 16) & 0b10000000) >> 7 == 1 if match.group('details') else None,
                 'address': match.group('address') or None,
                 'climb_rate': int(match.group('climb_rate')) * FPM_TO_MS if match.group('climb_rate') else None,
                 'turn_rate': float(match.group('turn_rate')) * HPM_TO_DEGS if match.group('turn_rate') else None,
                 'signal_quality': float(match.group('signal_quality')) if match.group('signal_quality') else None,
                 'error_count': int(match.group('error_count')) if match.group('error_count') else None,
                 'frequency_offset': float(match.group('frequency_offset')) if match.group('frequency_offset') else None,
                 'gps_quality': {
                     'horizontal': int(match.group('gps_quality_horizontal')),
                     'vertical': int(match.group('gps_quality_vertical'))} if match.group('gps_quality') else None,
                 'software_version': float(match.group('software_version')) if match.group('software_version') else None,
                 'hardware_version': int(match.group('hardware_version'), 16) if match.group('hardware_version') else None,
                 'real_address': match.group('real_address') or None,
                 'signal_power': float(match.group('signal_power')) if match.group('signal_power') else None}.items() if v is not None}
