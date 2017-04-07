import re
from datetime import datetime

from ogn.parser.utils import createTimestamp, parseAngle, kts2kmh, feet2m, fpm2ms
from ogn.parser.pattern import PATTERN_APRS_POSITION, PATTERN_APRS_STATUS, PATTERN_RECEIVER_BEACON, PATTERN_AIRCRAFT_BEACON
from ogn.parser.exceptions import AprsParseError, OgnParseError


def parse_aprs(message, reference_date=None, reference_time=None):
    if reference_date is None:
        now = datetime.utcnow()
        reference_date = now.date()
        reference_time = now.time()

    match_position = re.search(PATTERN_APRS_POSITION, message)
    if match_position:
        return {'name': match_position.group('callsign'),
                'receiver_name': match_position.group('receiver'),
                'dstcall': match_position.group('dstcall'),
                'timestamp': createTimestamp(match_position.group('time'), reference_date, reference_time),
                'latitude': parseAngle('0' + match_position.group('latitude') + (match_position.group('latitude_enhancement') or '0')) *
                (-1 if match_position.group('latitude_sign') == 'S' else 1),
                'symboltable': match_position.group('symbol_table'),
                'longitude': parseAngle(match_position.group('longitude') + (match_position.group('longitude_enhancement') or '0')) *
                (-1 if match_position.group('longitude_sign') == 'W' else 1),
                'symbolcode': match_position.group('symbol'),
                'track': int(match_position.group('course')) if match_position.group('course_extension') else 0,
                'ground_speed': int(match_position.group('ground_speed')) * kts2kmh if match_position.group('ground_speed') else 0,
                'altitude': int(match_position.group('altitude')) * feet2m,
                'comment': match_position.group('comment'),
                'beacon_type': 'receiver_beacon' if match_position.group('symbol_table') == 'I' and match_position.group('symbol') == '&' else 'aircraft_beacon'}

    match_status = re.search(PATTERN_APRS_STATUS, message)
    if match_status:
        return {'name': match_status.group('callsign'),
                'receiver_name': match_status.group('receiver'),
                'dstcall': match_status.group('dstcall'),
                'timestamp': createTimestamp(match_status.group('time'), reference_date, reference_time),
                'comment': match_status.group('comment'),
                'beacon_type': 'receiver_beacon'}

    raise AprsParseError(message)


def parse_ogn_aircraft_beacon(aprs_comment):
    ac_match = re.search(PATTERN_AIRCRAFT_BEACON, aprs_comment)
    if ac_match:
        return {'address_type': int(ac_match.group('details'), 16) & 0b00000011,
                'aircraft_type': (int(ac_match.group('details'), 16) & 0b01111100) >> 2,
                'stealth': (int(ac_match.group('details'), 16) & 0b10000000) >> 7 == 1,
                'address': ac_match.group('id'),
                'climb_rate': int(ac_match.group('climb_rate')) * fpm2ms if ac_match.group('climb_rate') else None,
                'turn_rate': float(ac_match.group('turn_rate')) if ac_match.group('turn_rate') else None,
                'flightlevel': float(ac_match.group('flight_level')) if ac_match.group('flight_level') else None,
                'signal_quality': float(ac_match.group('signal_quality')) if ac_match.group('signal_quality') else None,
                'error_count': float(ac_match.group('errors')) if ac_match.group('errors') else None,
                'frequency_offset': float(ac_match.group('frequency_offset')) if ac_match.group('frequency_offset') else None,
                'gps_status': ac_match.group('gps_accuracy') if ac_match.group('gps_accuracy') else None,
                'software_version': float(ac_match.group('flarm_software_version')) if ac_match.group('flarm_software_version') else None,
                'hardware_version': int(ac_match.group('flarm_hardware_version'), 16) if ac_match.group('flarm_hardware_version') else None,
                'real_address': ac_match.group('flarm_id') if ac_match.group('flarm_id') else None,
                'signal_power': float(ac_match.group('signal_power')) if ac_match.group('signal_power') else None}
    else:
        raise OgnParseError(aprs_comment)


def parse_ogn_receiver_beacon(aprs_comment):
    rec_match = re.search(PATTERN_RECEIVER_BEACON, aprs_comment)
    if rec_match:
        return {'version': rec_match.group('version') if rec_match.group('version') else None,
                'platform': rec_match.group('platform') if rec_match.group('platform') else None,
                'cpu_load': float(rec_match.group('cpu_load')) if rec_match.group('cpu_load') else None,
                'free_ram': float(rec_match.group('ram_free')) if rec_match.group('ram_free') else None,
                'total_ram': float(rec_match.group('ram_total')) if rec_match.group('ram_total') else None,
                'ntp_error': float(rec_match.group('ntp_offset')) if rec_match.group('ntp_offset') else None,
                'rt_crystal_correction': float(rec_match.group('ntp_correction')) if rec_match.group('ntp_correction') else None,
                'voltage': float(rec_match.group('voltage')) if rec_match.group('voltage') else None,
                'amperage': float(rec_match.group('amperage')) if rec_match.group('amperage') else None,
                'cpu_temp': float(rec_match.group('cpu_temperature')) if rec_match.group('cpu_temperature') else None,
                'senders_visible': int(rec_match.group('visible_senders')) if rec_match.group('visible_senders') else None,
                'senders_total': int(rec_match.group('senders')) if rec_match.group('senders') else None,
                'rec_crystal_correction': int(rec_match.group('rf_correction_manual')) if rec_match.group('rf_correction_manual') else 0,
                'rec_crystal_correction_fine': float(rec_match.group('rf_correction_automatic')) if rec_match.group('rf_correction_automatic') else 0.0,
                'rec_input_noise': float(rec_match.group('signal')) if rec_match.group('signal') else None,
                'senders_signal': float(rec_match.group('senders_signal')) if rec_match.group('senders_signal') else None,
                'senders_messages': float(rec_match.group('senders_messages')) if rec_match.group('senders_messages') else None,
                'good_senders_signal': float(rec_match.group('good_senders_signal')) if rec_match.group('good_senders_signal') else None,
                'good_senders': float(rec_match.group('good_senders')) if rec_match.group('good_senders') else None,
                'good_and_bad_senders': float(rec_match.group('good_and_bad_senders')) if rec_match.group('good_and_bad_senders') else None}
    else:
        raise OgnParseError(aprs_comment)


def parse(aprs_string, reference_date=None, reference_time=None):
    beacon = parse_aprs(aprs_string, reference_date, reference_time)
    if beacon['beacon_type'] == 'receiver_beacon':
        beacon.update(parse_ogn_receiver_beacon(beacon['comment']))
        return beacon
    elif beacon['beacon_type'] == 'aircraft_beacon':
        beacon.update(parse_ogn_aircraft_beacon(beacon['comment']))
        return beacon
    else:
        raise TypeError('This must not happen')
