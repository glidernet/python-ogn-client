from ogn.parser.pattern import PATTERN_SPIDER_POSITION_COMMENT

from .base import BaseParser


class SpiderParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'spider'
        self.position_pattern = PATTERN_SPIDER_POSITION_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)
        return {'spider_id': match.group('spider_id'),
                'signal_power': int(match.group('signal_power')) if match.group('signal_power') else None,
                'spider_registration': match.group('spider_registration') if match.group('spider_registration') else None,
                'gps_quality': match.group('gps_quality') if match.group('gps_quality') else None}
