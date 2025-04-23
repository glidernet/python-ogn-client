class BaseParser():
    def __init__(self):
        self.beacon_type = 'unknown'

    def parse(self, aprs_comment, aprs_type):
        if aprs_type.startswith('position'):
            data = self.parse_position(aprs_comment)
        elif aprs_type.startswith('status'):
            data = self.parse_status(aprs_comment)
        else:
            raise ValueError(f"aprs_type '{aprs_type}' unknown")
        data.update({'beacon_type': self.beacon_type})
        return data

    def parse_position(self, aprs_comment):
        raise NotImplementedError(f"Position parser for parser '{self.beacon_type}' not yet implemented")

    def parse_status(self, aprs_comment):
        raise NotImplementedError(f"Status parser for parser '{self.beacon_type}' not yet implemented")
