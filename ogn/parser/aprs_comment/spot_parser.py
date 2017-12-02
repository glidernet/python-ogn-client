from .base import BaseParser


class SpotParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'spot_beacon'
