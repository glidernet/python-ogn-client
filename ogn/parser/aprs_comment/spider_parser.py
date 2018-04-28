import re

from ogn.parser.pattern import PATTERN_SPIDER_POSITION_COMMENT

from .base import BaseParser


class SpiderParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'spider'

    @staticmethod
    def parse_position(aprs_comment):
        ac_match = re.search(PATTERN_SPIDER_POSITION_COMMENT, aprs_comment)
        return {'address': ac_match.group('id'),
                'signal_power': int(ac_match.group('signal_power')) if ac_match.group('signal_power') else None,
                'spider_id': ac_match.group('spider_id') if ac_match.group('spider_id') else None,
                'gps_quality': ac_match.group('gps_quality') if ac_match.group('gps_quality') else None}
