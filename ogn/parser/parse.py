from datetime import datetime, timezone

from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS, createTimestamp, parseAngle, KNOTS_TO_MS, KPH_TO_MS, FEETS_TO_METER, INCH_TO_MM, fahrenheit_to_celsius, CheapRuler, normalized_quality
from ogn.parser.pattern import PATTERN_APRS, PATTERN_APRS_POSITION, PATTERN_APRS_POSITION_WEATHER, PATTERN_APRS_STATUS, PATTERN_SERVER
from ogn.parser.exceptions import AprsParseError, OgnParseError

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
from ogn.parser.aprs_comment.safesky_parser import SafeskyParser
from ogn.parser.aprs_comment.microtrak_parser import MicrotrakParser
from ogn.parser.aprs_comment.generic_parser import GenericParser

from ogn_parser import parse as rust_parse

positions = {}
server_timestamp = None

mapping = {
    'OGCAPT': 'capturs',
    'OGNFNT': 'fanet',
    'OGFLR': 'flarm',
    'OGFLR6': 'flarm',
    'OGFLR7': 'flarm',
    'OGFLYM': 'flymaster',
    'OGNINRE': 'inreach',
    'OGLT24': 'lt24',
    'OGNMTK': 'microtrak',
    'OGNAVI': 'naviter',
    'OGNSDR': 'receiver',
    'OGNSKY': 'safesky',
    'OGPAW': 'pilot_aware',
    'OGSKYL': 'skylines',
    'OGSPID': 'spider',
    'OGSPOT': 'spot',
    'OGNTRK': 'tracker',
}


def parse(aprs_message, reference_timestamp=None, calculate_relations=False, use_server_timestamp=True, use_rust_parser=False):
    global server_timestamp

    if use_server_timestamp is True:
        reference_timestamp = server_timestamp or datetime.now(timezone.utc)
    elif reference_timestamp is None:
        reference_timestamp = datetime.now(timezone.utc)

    if use_rust_parser:
        rust_response = rust_parse(aprs_message)[0]
        message = {'raw_message': aprs_message, 'reference_timestamp': reference_timestamp}
        if parser_error := rust_response.get('parser_error'):
            message['aprs_type'] = 'comment'
            message['comment'] = str(parser_error)
        elif aprs_packet := rust_response.get('aprs_packet'):
            message.update({
                'aprs_type': 'position',
                'beacon_type': mapping.get(aprs_packet['to'], 'unknown'),
                'name': aprs_packet['from'],
                'dstcall': aprs_packet['to'],
            })
            if via := aprs_packet.get('via'):
                message['receiver_name'] = via[-1]
                if aprs_packet['via'][0] != 'TCPIP*' and aprs_packet['via'][0].endswith('*'): message['relay'] = aprs_packet['via'][0][:-1]
            if position := aprs_packet.get('position'):
                message.update({
                    'latitude': position['latitude'],
                    'longitude': position['longitude'],
                    'symboltable': position['symbol_table'],
                    'symbolcode': position['symbol_code'],
                })
                if 'timestamp' in position: message['timestamp'] = createTimestamp(position['timestamp'], reference_timestamp)

                if 'wind_direction' in position:
                    message['aprs_type'] = 'position_weather'
                    if 'wind_direction' in position: message["wind_direction"] = position['wind_direction']
                    if 'wind_speed' in position: message["wind_speed"] = position['wind_speed'] * KNOTS_TO_MS / KPH_TO_MS
                    if 'gust' in position: message['wind_speed_peak'] = position['gust'] * KNOTS_TO_MS / KPH_TO_MS
                    if 'temperature' in position: message['temperature'] = fahrenheit_to_celsius(position['temperature'])
                    if 'rainfall_1h' in position: message['rainfall_1h'] = position['rainfall_1h'] / 100.0 * INCH_TO_MM
                    if 'rainfall_24h' in position: message['rainfall_24h'] = position['rainfall_24h'] / 100.0 * INCH_TO_MM
                    if 'humidity' in position: message['humidity'] = 1. if position['humidity'] == 0 else position['humidity'] * 0.01
                    if 'barometric_pressure' in position: message['barometric_pressure'] = position['barometric_pressure']

                if 'course' in position: message["track"] = position['course']
                if 'speed' in position: message["ground_speed"] = position['speed'] * KNOTS_TO_MS / KPH_TO_MS
                if 'altitude' in position: message["altitude"] = position['altitude'] * FEETS_TO_METER

                if 'reserved' in position: message['reserved'] = position['reserved']
                if 'address_type' in position: message['address_type'] = position['address_type']
                if 'aircraft_type' in position: message['aircraft_type'] = position['aircraft_type']
                if 'is_notrack' in position: message['no-tracking'] = position['is_notrack']
                if 'is_stealth' in position: message['stealth'] = position['is_stealth']
                if 'address' in position: message['address'] = f"{position['address']:06X}"

                if 'climb_rate' in position: message["climb_rate"] = position['climb_rate'] * FPM_TO_MS
                if 'turn_rate' in position: message["turn_rate"] = position['turn_rate'] * HPM_TO_DEGS
                if 'signal_quality' in position: message["signal_quality"] = position['signal_quality']
                if 'error' in position: message["error_count"] = position['error']
                if 'frequency_offset' in position: message["frequency_offset"] = position['frequency_offset']
                if 'gps_quality' in position: message["gps_quality"] = position['gps_quality']
                if 'flight_level' in position: message["flightlevel"] = position['flight_level']
                if 'signal_power' in position: message["signal_power"] = position['signal_power']
                if 'software_version' in position: message["software_version"] = position['software_version']
                if 'hardware_version' in position: message["hardware_version"] = position['hardware_version']
                if 'original_address' in position: message["real_address"] = f"{position['original_address']:06X}"

                if 'unparsed' in position: message["user_comment"] = position['unparsed']

            elif status := aprs_packet.get('status'):
                message['aprs_type'] = 'status'
                if 'timestamp' in status: message['timestamp'] = createTimestamp(status['timestamp'], reference_timestamp)

                if 'version' in status: message["version"] = status['version']
                if 'platform' in status: message["platform"] = status['platform']
                if 'cpu_load' in status: message["cpu_load"] = status['cpu_load']
                if 'ram_free' in status: message["free_ram"] = status['ram_free']
                if 'ram_total' in status: message["total_ram"] = status['ram_total']
                if 'ntp_offset' in status: message["ntp_error"] = status['ntp_offset']
                if 'ntp_correction' in status: message["rt_crystal_correction"] = status['ntp_correction']
                if 'voltage' in status: message["voltage"] = status['voltage']
                if 'amperage' in status: message["amperage"] = status['amperage']
                if 'cpu_temperature' in status: message["cpu_temp"] = status['cpu_temperature']
                if 'visible_senders' in status: message["senders_visible"] = status['visible_senders']
                if 'latency' in status: message["latency"] = status['latency']
                if 'senders' in status: message["senders_total"] = status['senders']
                if 'rf_correction_manual' in status: message["rec_crystal_correction"] = status['rf_correction_manual']
                if 'rf_correction_automatic' in status: message["rec_crystal_correction_fine"] = status['rf_correction_automatic']
                if 'noise' in status: message["rec_input_noise"] = status['noise']
                if 'senders_signal_quality' in status: message["senders_signal"] = status['senders_signal_quality']
                if 'senders_messages' in status: message["senders_messages"] = status['senders_messages']
                if 'good_senders_signal_quality' in status: message["good_senders_signal"] = status['good_senders_signal_quality']
                if 'good_senders' in status: message["good_senders"] = status['good_senders']
                if 'good_and_bad_senders' in status: message["good_and_bad_senders"] = status['good_and_bad_senders']

                if 'unparsed' in status: message["user_comment"] = status['unparsed']
            else:
                raise ValueError("WTF")
        elif server_comment := rust_response.get('servercomment'):
            message.update({
                'version': server_comment['version'],
                'timestamp': datetime.strptime(server_comment['timestamp'], "%d %b %Y %H:%M:%S %Z"),
                'server': server_comment['server'],
                'ip_address': server_comment['ip_address'],
                'port': server_comment['port'],
                'aprs_type': 'server'})
        elif comment := rust_response.get('comment'):
            message.update({
                'comment': comment['comment'],
                'aprs_type': 'comment'})
        else:
            raise ValueError("WTF")

    else:
        message = parse_aprs(aprs_message, reference_timestamp=reference_timestamp)
        if message['aprs_type'] == 'position' or message['aprs_type'] == 'status':
            try:
                message.update(parse_comment(message['comment'], dstcall=message['dstcall'], aprs_type=message['aprs_type']))
            except Exception:
                raise OgnParseError(f"dstcall: {message['dstcall']}, aprs_type: {message['aprs_type']}, comment: {message['comment']}")

    if message['aprs_type'].startswith('position') and calculate_relations is True:
        positions[message['name']] = (message['longitude'], message['latitude'])
        if message['receiver_name'] in positions:
            cheap_ruler = CheapRuler((message['latitude'] + positions[message['receiver_name']][1]) / 2.0)
            message['distance'] = cheap_ruler.distance((message['longitude'], message['latitude']), positions[message['receiver_name']])
            message['bearing'] = cheap_ruler.bearing((message['longitude'], message['latitude']), positions[message['receiver_name']])
            message['normalized_quality'] = normalized_quality(message['distance'], message['signal_quality']) if 'signal_quality' in message else None

    if message['aprs_type'] == 'server':
        server_timestamp = message['timestamp']

    return message


def parse_aprs(message, reference_timestamp=None):
    if reference_timestamp is None:
        reference_timestamp = datetime.now(timezone.utc)

    result = {'raw_message': message,
              'reference_timestamp': reference_timestamp}

    if message and message[0] == '#':
        match_server = PATTERN_SERVER.search(message)
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
        match = PATTERN_APRS.search(message)
        if match:
            aprs_type = 'position' if match.group('aprs_type') == '/' else 'status' if match.group('aprs_type') == '>' else 'unknown'
            result.update({'aprs_type': aprs_type})
            aprs_body = match.group('aprs_body')
            if aprs_type == 'position':
                match_position = PATTERN_APRS_POSITION.search(aprs_body)
                if match_position:
                    result.update({
                        'name': match.group('callsign'),
                        'dstcall': match.group('dstcall'),
                        'relay': match.group('relay'),
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

                        'comment': match_position.group('comment') if match_position.group('comment') else "",
                    })
                    return result

                match_position_weather = PATTERN_APRS_POSITION_WEATHER.search(aprs_body)
                if match_position_weather:
                    result.update({
                        'aprs_type': 'position_weather',

                        'name': match.group('callsign'),
                        'dstcall': match.group('dstcall'),
                        'relay': match.group('relay'),
                        'receiver_name': match.group('receiver'),
                        'timestamp': createTimestamp(match_position_weather.group('time'), reference_timestamp),
                        'latitude': parseAngle('0' + match_position_weather.group('latitude')) *   # noqa: W504
                        (-1 if match_position_weather.group('latitude_sign') == 'S' else 1),
                        'symboltable': match_position_weather.group('symbol_table'),
                        'longitude': parseAngle(match_position_weather.group('longitude')) *   # noqa: W504
                        (-1 if match_position_weather.group('longitude_sign') == 'W' else 1),
                        'symbolcode': match_position_weather.group('symbol'),

                        'wind_direction': int(match_position_weather.group('wind_direction')) if match_position_weather.group('wind_direction') != '...' else None,
                        'wind_speed': int(match_position_weather.group('wind_speed')) * KNOTS_TO_MS / KPH_TO_MS if match_position_weather.group('wind_speed') != '...' else None,
                        'wind_speed_peak': int(match_position_weather.group('wind_speed_peak')) * KNOTS_TO_MS / KPH_TO_MS if match_position_weather.group('wind_speed_peak') != '...' else None,
                        'temperature': fahrenheit_to_celsius(float(match_position_weather.group('temperature'))) if match_position_weather.group('temperature') != '...' else None,
                        'rainfall_1h': int(match_position_weather.group('rainfall_1h')) / 100.0 * INCH_TO_MM if match_position_weather.group('rainfall_1h') else None,
                        'rainfall_24h': int(match_position_weather.group('rainfall_24h')) / 100.0 * INCH_TO_MM if match_position_weather.group('rainfall_24h') else None,
                        'humidity': int(match_position_weather.group('humidity')) * 0.01 if match_position_weather.group('humidity') else None,
                        'barometric_pressure': int(match_position_weather.group('barometric_pressure')) if match_position_weather.group('barometric_pressure') else None,

                        'comment': match_position_weather.group('comment') if match_position_weather.group('comment') else "",
                    })
                    return result

                raise AprsParseError(message)
            elif aprs_type == 'status':
                match_status = PATTERN_APRS_STATUS.search(aprs_body)
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
                          'OGFLR6': FlarmParser(),
                          'OGFLR7': FlarmParser(),
                          'OGNTRK': TrackerParser(),
                          'OGNSDR': ReceiverParser(),
                          'OGCAPT': GenericParser(beacon_type='capturs'),
                          'OGFLYM': GenericParser(beacon_type='flymaster'),
                          'OGNINRE': InreachParser(),
                          'OGLT24': LT24Parser(),
                          'OGNAVI': NaviterParser(),
                          'OGPAW': GenericParser(beacon_type='pilot_aware'),
                          'OGSKYL': SkylinesParser(),
                          'OGSPID': SpiderParser(),
                          'OGSPOT': SpotParser(),
                          'OGNSKY': SafeskyParser(),
                          'OGNMTK': MicrotrakParser(),
                          'GENERIC': GenericParser(beacon_type='unknown'),
                          }


def parse_comment(aprs_comment, dstcall='APRS', aprs_type="position"):
    parser = dstcall_parser_mapping.get(dstcall)
    if parser:
        return parser.parse(aprs_comment, aprs_type)
    else:
        return dstcall_parser_mapping.get('GENERIC').parse(aprs_comment, aprs_type)
