import re

from ogn.parser.pattern import PATTERN_SPOT_BEACON

from .base import BaseParser


class SpotParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'spot'

    @staticmethod
    def parse_position(aprs_comment):
        ac_match = re.search(PATTERN_SPOT_BEACON, aprs_comment)
        return {'id': ac_match.group('id'),
                'model': int(ac_match.group('model')) if ac_match.group('model') else None,
                'status': ac_match.group('status') if ac_match.group('status') else None}
