import re
from datetime import datetime

from ogn.parser.utils import createTimestamp, parseAngle, kts2kmh, feet2m
from ogn.parser.pattern import PATTERN_APRS_POSITION, PATTERN_APRS_STATUS
from ogn.parser.exceptions import AprsParseError, OgnParseError

from ogn.parser.parse_ogn import parse_aircraft_beacon, parse_receiver_beacon
from ogn.parser.parse_naviter import parse as parse_naviter_beacon
from ogn.parser.parse_lt24 import parse as parse_lt24_beacon
from ogn.parser.parse_spider import parse as parse_spider_beacon
from ogn.parser.parse_spot import parse as parse_spot_beacon
from ogn.parser.parse_skylines import parse as parse_skylines_beacon
from ogn.parser.parse_tracker import parse_position as parse_tracker_position
from ogn.parser.parse_tracker import parse_status as parse_tracker_status
from ogn.parser.parse_receiver import parse_position as parse_receiver_position
from ogn.parser.parse_receiver import parse_status as parse_receiver_status


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
        if not aprs_comment:
            return {'beacon_type': 'receiver_beacon'}

        ac_data = parse_aircraft_beacon(aprs_comment)
        if ac_data:
            ac_data.update({'beacon_type': 'aircraft_beacon'})
            return ac_data

        rc_data = parse_receiver_beacon(aprs_comment)
        if rc_data:
            rc_data.update({'beacon_type': 'receiver_beacon'})
            return rc_data
        else:
            return {'user_comment': aprs_comment,
                    'beacon_type': 'receiver_beacon'}
    elif dstcall == "OGFLR":
        ac_data = parse_aircraft_beacon(aprs_comment)
        ac_data.update({'beacon_type': 'aircraft_beacon'})
        return ac_data
    elif dstcall == "OGNTRK":
        if aprs_type == "position":
            data = parse_tracker_position(aprs_comment)
            data.update({'beacon_type': 'aircraft_beacon'})
        elif aprs_type == "status":
            data = parse_tracker_status(aprs_comment)
            data.update({'beacon_type': 'aircraft_beacon'})
        return data
    elif dstcall == "OGNSDR":
        if aprs_type == "position":
            data = parse_receiver_position(aprs_comment)
            data.update({'beacon_type': 'receiver_beacon'})
        elif aprs_type == "status":
            data = parse_receiver_status(aprs_comment)
            data.update({'beacon_type': 'receiver_beacon'})
        return data
    elif dstcall == "OGLT24":
        ac_data = parse_lt24_beacon(aprs_comment)
        ac_data.update({'beacon_type': 'lt24_beacon'})
        return ac_data
    elif dstcall == "OGNAVI":
        ac_data = parse_naviter_beacon(aprs_comment)
        ac_data.update({'beacon_type': 'naviter_beacon'})
        return ac_data
    elif dstcall == "OGSKYL":
        ac_data = parse_skylines_beacon(aprs_comment)
        ac_data.update({'beacon_type': 'skylines_beacon'})
        return ac_data
    elif dstcall == "OGSPID":
        ac_data = parse_spider_beacon(aprs_comment)
        ac_data.update({'beacon_type': 'spider_beacon'})
        return ac_data
    elif dstcall == "OGSPOT":
        ac_data = parse_spot_beacon(aprs_comment)
        ac_data.update({'beacon_type': 'spot_beacon'})
        return ac_data
    else:
        raise OgnParseError("No parser for dstcall {} found. APRS comment: {}".format(dstcall, aprs_comment))
