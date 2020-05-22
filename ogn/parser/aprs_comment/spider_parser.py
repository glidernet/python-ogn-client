from ogn.parser.pattern import PATTERN_SPIDER_POSITION_COMMENT

from .base import BaseParser


class SpiderParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'spider'
        self.position_pattern = PATTERN_SPIDER_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        ac_match = self.position_pattern.match(aprs_comment)
        return {'spider_id': ac_match.group('spider_id'),
                'signal_power': int(ac_match.group('signal_power')) if ac_match.group('signal_power') else None,
                'spider_registration': ac_match.group('spider_registration') if ac_match.group('spider_registration') else None,
                'gps_quality': ac_match.group('gps_quality') if ac_match.group('gps_quality') else None}
