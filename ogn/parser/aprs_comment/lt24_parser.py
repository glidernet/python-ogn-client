import re

from ogn.parser.utils import fpm2ms
from ogn.parser.pattern import PATTERN_LT24_BEACON

from .base import BaseParser


class LT24Parser(BaseParser):
    def __init__(self):
        self.beacon_type = 'lt24'

    @staticmethod
    def parse_position(aprs_comment):
        ac_match = re.search(PATTERN_LT24_BEACON, aprs_comment)
        return {'id': ac_match.group('id'),
                'climb_rate': int(ac_match.group('climb_rate')) * fpm2ms if ac_match.group('climb_rate') else None,
                'source': ac_match.group('source') if ac_match.group('source') else None}
