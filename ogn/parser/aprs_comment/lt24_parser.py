from ogn.parser.utils import FPM_TO_MS
from ogn.parser.pattern import PATTERN_LT24_POSITION_COMMENT

from .base import BaseParser


class LT24Parser(BaseParser):
    def __init__(self):
        self.beacon_type = 'lt24'
        self.position_pattern = PATTERN_LT24_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)
        return {'lt24_id': match.group('lt24_id'),
                'climb_rate': int(match.group('climb_rate')) * FPM_TO_MS if match.group('climb_rate') else None,
                'source': match.group('source') if match.group('source') else None}
