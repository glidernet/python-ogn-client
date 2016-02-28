"""
exception definitions
"""
from datetime import datetime


class ParseError(Exception):
    pass


class AprsParseError(ParseError):
    """Parse error while parsing an aprs packet."""
    def __init__(self, aprs_string):
        self.aprs_string = aprs_string

        self.message = "This is not a valid APRS packet: {}".format(aprs_string)
        super(AprsParseError, self).__init__(self.message)


class OgnParseError(ParseError):
    """Parse error while parsing an ogn message from aprs comment."""
    def __init__(self, aprs_comment):
        self.aprs_comment = aprs_comment

        self.message = "This is not a valid OGN message: {}".format(aprs_comment)
        super(OgnParseError, self).__init__(self.message)


class AmbigousTimeError(ParseError):
    """Timstamp from the past/future, can't fully reconstruct datetime from timestamp."""
    def __init__(self, reference, packet_time):
        self.reference = reference
        self.packet_time = packet_time
        self.timedelta = reference - datetime.combine(reference, packet_time)

        self.message = "Can't reconstruct timstamp, {:.0f}s from past.".format(self.timedelta.total_seconds())
        super(AmbigousTimeError, self).__init__(self.message)
