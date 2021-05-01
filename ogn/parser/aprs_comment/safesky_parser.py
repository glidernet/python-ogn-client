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
        result.update(
            {'safesky_id': match.group('safesky_id'),
             'climb_rate': int(match.group('climb_rate')) * FPM_TO_MS if match.group('climb_rate') else None})
        if match.group('gps_quality'):
            result.update({
                'gps_quality': {
                    'horizontal': int(match.group('gps_quality_horizontal')),
                    'vertical': int(match.group('gps_quality_vertical'))
                }
            })
        return result
