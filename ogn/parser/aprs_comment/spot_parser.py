import re

from ogn.parser.pattern import PATTERN_SPOT_POSITION_COMMENT

from .base import BaseParser


class SpotParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'spot'
        self.position_pattern = re.compile(PATTERN_SPOT_POSITION_COMMENT)

    def parse_position(self, aprs_comment):
        ac_match = self.position_pattern.match(aprs_comment)
        return {'address': ac_match.group('id'),
                'model': ac_match.group('model') if ac_match.group('model') else None,
                'status': ac_match.group('status') if ac_match.group('status') else None}
