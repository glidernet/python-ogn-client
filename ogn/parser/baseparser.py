class BaseParser():
    beacon_type = "undefined"

    @staticmethod
    def parse(aprs_comment, aprs_type):
        if aprs_type == "position":
            data = __class__.parse_position(aprs_comment)
        elif aprs_type == "status":
            data = __class__.parse_status(aprs_comment)
        else:
            raise ValueError("aprs_type {} unknown".format(aprs_type))
        data.update({'beacon_type': __class__.beacon_type})
        return data

    @staticmethod
    def parse_position(aprs_comment):
        raise NotImplementedError("Position parser for parser '{}' not yet implemented".format(__class__.__name__))

    @staticmethod
    def parse_status(aprs_comment):
        raise NotImplementedError("Status parser for parser '{}' not yet implemented".format(__class__.__name__))
