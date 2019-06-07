import re

from ogn.parser.pattern import PATTERN_INREACH_POSITION_COMMENT

from .base import BaseParser


class InreachParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'inreach'
        self.position_pattern = re.compile(PATTERN_INREACH_POSITION_COMMENT)

    def parse_position(self, aprs_comment):
        ac_match = self.position_pattern.match(aprs_comment)
        return {'address': ac_match.group('id'),
                'model': ac_match.group('model') if ac_match.group('model') else None,
                'status': ac_match.group('status') == 'True' if ac_match.group('status') else None,
                'pilot_name': ac_match.group('pilot_name') if ac_match.group('pilot_name') else None}
