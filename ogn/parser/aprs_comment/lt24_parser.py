import re

from ogn.parser.utils import FPM_TO_MS
from ogn.parser.pattern import PATTERN_LT24_POSITION_COMMENT

from .base import BaseParser


class LT24Parser(BaseParser):
    def __init__(self):
        self.beacon_type = 'lt24'

    @staticmethod
    def parse_position(aprs_comment):
        ac_match = re.search(PATTERN_LT24_POSITION_COMMENT, aprs_comment)
        return {'address': ac_match.group('id'),
                'climb_rate': int(ac_match.group('climb_rate')) * FPM_TO_MS if ac_match.group('climb_rate') else None,
                'source': ac_match.group('source') if ac_match.group('source') else None}
