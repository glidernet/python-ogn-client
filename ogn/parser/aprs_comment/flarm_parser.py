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

        def if_present(arg, func):
            result = ac_match.group(arg)
            return (func(result)) if result else None

        return {'address_type': if_present('details', lambda x: int(x, 16) & 0b00000011),
                'aircraft_type': if_present('details', lambda x: (int(x, 16) & 0b01111100) >> 2),
                'stealth': if_present('details', lambda x: (int(x, 16) & 0b10000000) >> 7 == 1),
                'address': if_present('address', lambda x: x),
                'climb_rate': if_present('climb_rate', lambda x: int(x) * FPM_TO_MS),
                'turn_rate': if_present('turn_rate', lambda x: float(x) * HPM_TO_DEGS),
                'signal_quality': if_present('signal_quality', float),
                'error_count': if_present('error_count', int),
                'frequency_offset': if_present('frequency_offset', float),
                'gps_quality': if_present('gps_quality', lambda _x: {
                    'horizontal': int(ac_match.group('gps_quality_horizontal')),
                    'vertical': int(ac_match.group('gps_quality_vertical'))}),
                'software_version': if_present('software_version', float),
                'hardware_version': if_present('hardware_version', lambda x: int(x, 16)),
                'real_address': if_present('real_address', lambda x: x),
                'signal_power': if_present('signal_power', float),
                }
