from .base import BaseParser


class LT24Parser(BaseParser):
    def __init__(self):
        self.beacon_type = 'lt24_beacon'
