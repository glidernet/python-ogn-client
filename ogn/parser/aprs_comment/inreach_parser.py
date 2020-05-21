from ogn.parser.pattern import PATTERN_INREACH_POSITION_COMMENT

from .base import BaseParser


class InreachParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'inreach'
        self.position_pattern = PATTERN_INREACH_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)
        return {'address': match.group('id'),
                'model': match.group('model') if match.group('model') else None,
                'status': match.group('status') == 'True' if match.group('status') else None,
                'pilot_name': match.group('pilot_name') if match.group('pilot_name') else None}
