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
                'comment': match_position.group('comment')}

    match_status = re.search(PATTERN_APRS_STATUS, message)
    if match_status:
        return {'name': match_status.group('callsign'),
                'receiver_name': match_status.group('receiver'),
                'dstcall': match_status.group('dstcall'),
                'timestamp': createTimestamp(match_status.group('time'), reference_date, reference_time),
                'comment': match_status.group('comment')}

    raise AprsParseError(message)


def parse_ogn_aircraft_beacon(aprs_comment):
    ac_match = re.search(PATTERN_AIRCRAFT_BEACON, aprs_comment)
    if ac_match:
        return {'address_type': int(ac_match.group('details'), 16) & 0b00000011,
                'aircraft_type': (int(ac_match.group('details'), 16) & 0b01111100) >> 2,
                'stealth': (int(ac_match.group('details'), 16) & 0b10000000) >> 7 == 1,
                'address': ac_match.group('id'),
                'climb_rate': int(ac_match.group('climb_rate')) * fpm2ms,
                'turn_rate': float(ac_match.group('turn_rate')),
                'flightlevel': float(ac_match.group('flight_level')) if ac_match.group('flight_level') else None,
                'signal_strength': float(ac_match.group('signal')),
                'error_count': float(ac_match.group('errors')),
                'frequency_offset': float(ac_match.group('frequency_offset')),
                'gps_status': ac_match.group('gps_accuracy'),
                'software_version': float(ac_match.group('flarm_software_version')) if ac_match.group('flarm_software_version') else None,
                'hardware_version': int(ac_match.group('flarm_hardware_version'), 16) if ac_match.group('flarm_hardware_version') else None,
                'real_address': ac_match.group('flarm_id')}
    else:
        return None


def parse_ogn_receiver_beacon(aprs_comment):
    rec_match = re.search(PATTERN_RECEIVER_BEACON, aprs_comment)
    if rec_match:
        return {'version': rec_match.group('version'),
                'platform': rec_match.group('platform'),
                'cpu_load': float(rec_match.group('cpu_load')),
                'free_ram': float(rec_match.group('ram_free')),
                'total_ram': float(rec_match.group('ram_total')),
                'ntp_error': float(rec_match.group('ntp_offset')),
                'rt_crystal_correction': float(rec_match.group('ntp_correction')),
                'cpu_temp': float(rec_match.group('cpu_temperature')) if rec_match.group('cpu_temperature') else None,
                'aircraft_counter_visible': int(rec_match.group('aircraft_counter_visible')) if rec_match.group('aircraft_counter_visible') else None,
                'aircraft_counter_total': int(rec_match.group('aircraft_counter_total')) if rec_match.group('aircraft_counter_total') else None,
                'rec_crystal_correction': int(rec_match.group('manual_correction')) if rec_match.group('manual_correction') else 0,
                'rec_crystal_correction_fine': float(rec_match.group('automatic_correction')) if rec_match.group('automatic_correction') else 0.0,
                'rec_input_noise': float(rec_match.group('input_noise')) if rec_match.group('input_noise') else None,
                'total_snr': float(rec_match.group('total_snr')) if rec_match.group('total_snr') else None,
                'total_fixes': float(rec_match.group('total_fixes')) if rec_match.group('total_fixes') else None,
                'daily_snr_selection': float(rec_match.group('daily_snr_selection')) if rec_match.group('daily_snr_selection') else None,
                'daily_devices_selection': float(rec_match.group('daily_devices_selection')) if rec_match.group('daily_devices_selection') else None,
                'daily_devices': float(rec_match.group('daily_devices')) if rec_match.group('daily_devices') else None}
    else:
        return None


def parse_ogn_beacon(aprs_comment):
    ac_data = parse_ogn_aircraft_beacon(aprs_comment)
    if ac_data:
        ac_data.update({'beacon_type': 'aircraft_beacon'})
        return ac_data

    rc_data = parse_ogn_receiver_beacon(aprs_comment)
    if rc_data:
        rc_data.update({'beacon_type': 'receiver_beacon'})
        return rc_data

    raise OgnParseError(aprs_comment)
