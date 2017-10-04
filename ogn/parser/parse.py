import re
from datetime import datetime

from ogn.parser.utils import createTimestamp, parseAngle, kts2kmh, feet2m
from ogn.parser.pattern import PATTERN_APRS_POSITION, PATTERN_APRS_STATUS
from ogn.parser.exceptions import AprsParseError, OgnParseError

from ogn.parser.parse_ogn import APRS
from ogn.parser.parse_lt24 import OGLT24
from ogn.parser.parse_naviter import OGNAVI
from ogn.parser.parse_flarm import OGFLR
from ogn.parser.parse_tracker import OGNTRK
from ogn.parser.parse_receiver import OGNSDR
from ogn.parser.parse_skylines import OGSKYL
from ogn.parser.parse_spider import OGSPID
from ogn.parser.parse_spot import OGSPOT


def parse(aprs_message, reference_date=None, reference_time=None):
    if reference_date is None:
        now = datetime.utcnow()
        reference_date = now.date()
        reference_time = now.time()

    message = parse_aprs(aprs_message, reference_date, reference_time)
    message.update(parse_comment(message['comment'], dstcall=message['dstcall'], aprs_type=message['aprs_type']))
    return message


def parse_aprs(message, reference_date, reference_time=None):
    match_position = re.search(PATTERN_APRS_POSITION, message)
    if match_position:
        return {'name': match_position.group('callsign'),
                'dstcall': match_position.group('dstcall'),
                'relay': match_position.group('relay') if match_position.group('relay') else None,
                'receiver_name': match_position.group('receiver'),
                'timestamp': createTimestamp(match_position.group('time'), reference_date, reference_time),
                'latitude': parseAngle('0' + match_position.group('latitude') + (match_position.group('latitude_enhancement') or '0')) *
                (-1 if match_position.group('latitude_sign') == 'S' else 1),
                'symboltable': match_position.group('symbol_table'),
                'longitude': parseAngle(match_position.group('longitude') + (match_position.group('longitude_enhancement') or '0')) *
                (-1 if match_position.group('longitude_sign') == 'W' else 1),
                'symbolcode': match_position.group('symbol'),
                'track': int(match_position.group('course')) if match_position.group('course_extension') else None,
                'ground_speed': int(match_position.group('ground_speed')) * kts2kmh if match_position.group('ground_speed') else None,
                'altitude': int(match_position.group('altitude')) * feet2m,
                'comment': match_position.group('comment') if match_position.group('comment') else "",
                'aprs_type': 'position'}

    match_status = re.search(PATTERN_APRS_STATUS, message)
    if match_status:
        return {'name': match_status.group('callsign'),
                'dstcall': match_status.group('dstcall'),
                'receiver_name': match_status.group('receiver'),
                'timestamp': createTimestamp(match_status.group('time'), reference_date, reference_time),
                'comment': match_status.group('comment') if match_status.group('comment') else "",
                'aprs_type': 'status'}

    raise AprsParseError(message)


def parse_comment(aprs_comment, dstcall="APRS", aprs_type="position"):
    if dstcall == "APRS":   # this can be a receiver or an aircraft
        return APRS.parse(aprs_comment, aprs_type)
    elif dstcall == "OGFLR":
        return OGFLR.parse(aprs_comment, aprs_type)
    elif dstcall == "OGNTRK":
        return OGNTRK.parse(aprs_comment, aprs_type)
    elif dstcall == "OGNSDR":
        return OGNSDR.parse(aprs_comment, aprs_type)
    elif dstcall == "OGLT24":
        return OGLT24.parse(aprs_comment, aprs_type)
    elif dstcall == "OGNAVI":
        return OGNAVI.parse(aprs_comment, aprs_type)
    elif dstcall == "OGSKYL":
        return OGSKYL.parse(aprs_comment, aprs_type)
    elif dstcall == "OGSPID":
        return OGSPID.parse(aprs_comment, aprs_type)
    elif dstcall == "OGSPOT":
        return OGSPOT.parse(aprs_comment, aprs_type)
    else:
        raise OgnParseError("No parser for dstcall {} found. APRS comment: {}".format(dstcall, aprs_comment))
