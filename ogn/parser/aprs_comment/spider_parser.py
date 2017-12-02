from .base import BaseParser


class SpiderParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'spider_beacon'
