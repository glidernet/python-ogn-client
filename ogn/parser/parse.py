import re
from datetime import datetime

from ogn.parser.utils import createTimestamp, parseAngle, KNOTS_TO_MS, KPH_TO_MS, FEETS_TO_METER
from ogn.parser.pattern import PATTERN_APRS, PATTERN_APRS_POSITION, PATTERN_APRS_STATUS, PATTERN_SERVER
from ogn.parser.exceptions import AprsParseError

from ogn.parser.aprs_comment.ogn_parser import OgnParser
from ogn.parser.aprs_comment.fanet_parser import FanetParser
from ogn.parser.aprs_comment.lt24_parser import LT24Parser
from ogn.parser.aprs_comment.naviter_parser import NaviterParser
from ogn.parser.aprs_comment.flarm_parser import FlarmParser
from ogn.parser.aprs_comment.tracker_parser import TrackerParser
from ogn.parser.aprs_comment.receiver_parser import ReceiverParser
from ogn.parser.aprs_comment.skylines_parser import SkylinesParser
from ogn.parser.aprs_comment.spider_parser import SpiderParser
from ogn.parser.aprs_comment.spot_parser import SpotParser
from ogn.parser.aprs_comment.inreach_parser import InreachParser
from ogn.parser.aprs_comment.generic_parser import GenericParser


def parse(aprs_message, reference_timestamp=None):
    if reference_timestamp is None:
        reference_timestamp = datetime.utcnow()

    message = parse_aprs(aprs_message, reference_timestamp)
    if message['aprs_type'] == 'position' or message['aprs_type'] == 'status':
        message.update(parse_comment(message['comment'],
                                     dstcall=message['dstcall'],
                                     aprs_type=message['aprs_type']))
    return message


def parse_aprs(message, reference_timestamp=None):
    if reference_timestamp is None:
        reference_timestamp = datetime.utcnow()

    result = {'raw_message': message,
              'reference_timestamp': reference_timestamp}

    if message and message[0] == '#':
        match_server = re.search(PATTERN_SERVER, message)
        if match_server:
            result.update({
                'version': match_server.group('version'),
                'timestamp': datetime.strptime(match_server.group('timestamp'), "%d %b %Y %H:%M:%S %Z"),
                'server': match_server.group('server'),
                'ip_address': match_server.group('ip_address'),
                'port': match_server.group('port'),
                'aprs_type': 'server'})
        else:
            result.update({
                'comment': message,
                'aprs_type': 'comment'})

    else:
        match = re.search(PATTERN_APRS, message)
        if match:
            aprs_type = 'position' if match.group('aprs_type') == '/' else 'status' if match.group('aprs_type') == '>' else 'unknown'
            result.update({'aprs_type': aprs_type})
            aprs_body = match.group('aprs_body')
            if aprs_type == 'position':
                match_position = re.search(PATTERN_APRS_POSITION, aprs_body)
                if match_position:
                    result.update({
                        'name': match.group('callsign'),
                        'dstcall': match.group('dstcall'),
                        'relay': match.group('relay') if match.group('relay') else None,
                        'receiver_name': match.group('receiver'),
                        'timestamp': createTimestamp(match_position.group('time'), reference_timestamp),
                        'latitude': parseAngle('0' + match_position.group('latitude') + (match_position.group('latitude_enhancement') or '0')) *   # noqa: W504
                        (-1 if match_position.group('latitude_sign') == 'S' else 1),
                        'symboltable': match_position.group('symbol_table'),
                        'longitude': parseAngle(match_position.group('longitude') + (match_position.group('longitude_enhancement') or '0')) *   # noqa: W504
                        (-1 if match_position.group('longitude_sign') == 'W' else 1),
                        'symbolcode': match_position.group('symbol'),
                        'track': int(match_position.group('course')) if match_position.group('course_extension') else None,
                        'ground_speed': int(match_position.group('ground_speed')) * KNOTS_TO_MS / KPH_TO_MS if match_position.group('ground_speed') else None,
                        'altitude': int(match_position.group('altitude')) * FEETS_TO_METER if match_position.group('altitude') else None,
                        'comment': match_position.group('comment') if match_position.group('comment') else ""})
                else:
                    raise AprsParseError(message)
            elif aprs_type == 'status':
                match_status = re.search(PATTERN_APRS_STATUS, aprs_body)
                if match_status:
                    result.update({
                        'name': match.group('callsign'),
                        'dstcall': match.group('dstcall'),
                        'receiver_name': match.group('receiver'),
                        'timestamp': createTimestamp(match_status.group('time'), reference_timestamp),
                        'comment': match_status.group('comment') if match_status.group('comment') else ""})
                else:
                    raise NotImplementedError(message)
        else:
            raise AprsParseError(message)

    return result


dstcall_parser_mapping = {'APRS': OgnParser(),
                          'OGNFNT': FanetParser(),
                          'OGFLR': FlarmParser(),
                          'OGNTRK': TrackerParser(),
                          'OGNSDR': ReceiverParser(),
                          'OGCAPT': GenericParser(beacon_type='capturs'),
                          'OGFLYM': GenericParser(beacon_type='flymaster'),
                          'OGINREACH': InreachParser(),
                          'OGLT24': LT24Parser(),
                          'OGNAVI': NaviterParser(),
                          'OGPAW': GenericParser(beacon_type='pilot_aware'),
                          'OGSKYL': SkylinesParser(),
                          'OGSPID': SpiderParser(),
                          'OGSPOT': SpotParser(),
                          'GENERIC': GenericParser(beacon_type='unknown'),
                          }


def parse_comment(aprs_comment, dstcall='APRS', aprs_type="position"):
    parser = dstcall_parser_mapping.get(dstcall)
    if parser:
        return parser.parse(aprs_comment, aprs_type)
    else:
        return dstcall_parser_mapping.get('GENERIC').parse(aprs_comment, aprs_type)
