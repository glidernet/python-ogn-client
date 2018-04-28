import re

from ogn.parser.utils import fpm2ms
from ogn.parser.pattern import PATTERN_SKYLINES_POSITION_COMMENT

from .base import BaseParser


class SkylinesParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'skylines'

    @staticmethod
    def parse_position(aprs_comment):
        ac_match = re.search(PATTERN_SKYLINES_POSITION_COMMENT, aprs_comment)
        return {'address': ac_match.group('id'),
                'climb_rate': int(ac_match.group('climb_rate')) * fpm2ms if ac_match.group('climb_rate') else None}
