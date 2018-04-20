import re

from ogn.parser.pattern import PATTERN_FLARM_POSITION_COMMENT
from ogn.parser.utils import fpm2ms

from .base import BaseParser


class FlarmParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'flarm'

    @staticmethod
    def parse_position(aprs_comment):
        ac_match = re.search(PATTERN_FLARM_POSITION_COMMENT, aprs_comment)
        return {'address_type': int(ac_match.group('details'), 16) & 0b00000011,
                'aircraft_type': (int(ac_match.group('details'), 16) & 0b01111100) >> 2,
                'stealth': (int(ac_match.group('details'), 16) & 0b10000000) >> 7 == 1,
                'address': ac_match.group('id'),
                'climb_rate': int(ac_match.group('climb_rate')) * fpm2ms,
                'turn_rate': float(ac_match.group('turn_rate')),
                'signal_quality': float(ac_match.group('signal_quality')),
                'error_count': int(ac_match.group('errors')),
                'frequency_offset': float(ac_match.group('frequency_offset')),
                'gps_status': ac_match.group('gps_accuracy') if ac_match.group('gps_accuracy') else None,
                'software_version': float(ac_match.group('flarm_software_version')) if ac_match.group('flarm_software_version') else None,
                'hardware_version': int(ac_match.group('flarm_hardware_version'), 16) if ac_match.group('flarm_hardware_version') else None,
                'real_address': ac_match.group('flarm_id') if ac_match.group('flarm_id') else None,
                'signal_power': float(ac_match.group('signal_power')) if ac_match.group('signal_power') else None}
