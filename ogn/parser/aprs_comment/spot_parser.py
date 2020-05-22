from ogn.parser.pattern import PATTERN_SPOT_POSITION_COMMENT

from .base import BaseParser


class SpotParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'spot'
        self.position_pattern = PATTERN_SPOT_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)
        return {'spot_id': match.group('spot_id'),
                'model': match.group('model') if match.group('model') else None,
                'status': match.group('status') if match.group('status') else None}
