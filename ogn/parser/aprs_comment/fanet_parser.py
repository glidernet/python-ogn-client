import re

from ogn.parser.utils import fpm2ms
from ogn.parser.pattern import PATTERN_FANET_POSITION_COMMENT

from .base import BaseParser


class FanetParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'fanet'

    @staticmethod
    def parse_position(aprs_comment):
        ac_match = re.search(PATTERN_FANET_POSITION_COMMENT, aprs_comment)
        return {'id': ac_match.group('id') if ac_match.group('id') else None,
                'climb_rate': int(ac_match.group('climb_rate')) * fpm2ms if ac_match.group('climb_rate') else None}
