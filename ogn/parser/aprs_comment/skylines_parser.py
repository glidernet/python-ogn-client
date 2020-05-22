from ogn.parser.utils import FPM_TO_MS
from ogn.parser.pattern import PATTERN_SKYLINES_POSITION_COMMENT

from .base import BaseParser


class SkylinesParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'skylines'
        self.position_pattern = PATTERN_SKYLINES_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)
        return {'skylines_id': match.group('skylines_id'),
                'climb_rate': int(match.group('climb_rate')) * FPM_TO_MS if match.group('climb_rate') else None}
