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


def parse_aprs(message, reference_date=None, reference_time=None):
    if reference_date is None:
        now = datetime.utcnow()
        reference_date = now.date()
        reference_time = now.time()

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
                'comment': match_position.group('comment'),
                'aprs_type': 'position'}

    match_status = re.search(PATTERN_APRS_STATUS, message)
    if match_status:
        return {'name': match_status.group('callsign'),
                'dstcall': match_status.group('dstcall'),
                'receiver_name': match_status.group('receiver'),
                'timestamp': createTimestamp(match_status.group('time'), reference_date, reference_time),
                'comment': match_status.group('comment'),
                'aprs_type': 'status'}

    raise AprsParseError(message)


def parse_ogn_beacon(aprs_comment, dstcall="APRS"):
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

        raise OgnParseError(aprs_comment)
    elif dstcall == "OGFLR":
        ac_data = parse_aircraft_beacon(aprs_comment)
        ac_data.update({'beacon_type': 'aircraft_beacon'})
        return ac_data
    elif dstcall == "OGNTRK":
        ac_data = parse_aircraft_beacon(aprs_comment)
        ac_data.update({'beacon_type': 'aircraft_beacon'})
        return ac_data
    elif dstcall == "OGNSDR":
        ac_data = parse_receiver_beacon(aprs_comment)
        ac_data.update({'beacon_type': 'receiver_beacon'})
        return ac_data
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
        raise ValueError("dstcall {} unknown".format(dstcall))
