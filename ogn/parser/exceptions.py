"""
exception definitions
"""


class AprsParseError(Exception):
    """Parse error while parsing an aprs packet."""
    def __init__(self, aprs_string):
        self.aprs_string = aprs_string

        self.message = f"This is not a valid APRS packet: {aprs_string}"
