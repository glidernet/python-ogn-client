class BaseParser():
    def __init__(self):
        self.beacon_type = 'unknown'

    def parse(self, aprs_comment, aprs_type):
        if aprs_type.startswith('position'):
            data = self.parse_position(aprs_comment)
        elif aprs_type.startswith('status'):
            data = self.parse_status(aprs_comment)
        else:
            raise ValueError("aprs_type {} unknown".format(aprs_type))
        data.update({'beacon_type': self.beacon_type})
        return data

    def parse_position(self, aprs_comment):
        raise NotImplementedError("Position parser for parser '{}' not yet implemented".format(self.beacon_type))

    def parse_status(self, aprs_comment):
        raise NotImplementedError("Status parser for parser '{}' not yet implemented".format(self.beacon_type))
