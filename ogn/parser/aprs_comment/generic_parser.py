from .base import BaseParser


class GenericParser(BaseParser):
    def __init__(self, beacon_type='unknown'):
        self.beacon_type = beacon_type

    def parse_position(self, aprs_comment):
        return {'comment': aprs_comment}

    def parse_status(self, aprs_comment):
        return {'comment': aprs_comment}
