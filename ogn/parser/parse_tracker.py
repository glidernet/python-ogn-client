import re

from ogn.parser.utils import fpm2ms
from ogn.parser.pattern import PATTERN_TRACKER_BEACON_POSITION, PATTERN_TRACKER_BEACON_STATUS


def parse_position(aprs_comment):
    match = re.search(PATTERN_TRACKER_BEACON_POSITION, aprs_comment)
    return {'address_type': int(match.group('details'), 16) & 0b00000011,
            'aircraft_type': (int(match.group('details'), 16) & 0b01111100) >> 2,
            'stealth': (int(match.group('details'), 16) & 0b10000000) >> 7 == 1,
            'address': match.group('id'),
            'climb_rate': int(match.group('climb_rate')) * fpm2ms if match.group('climb_rate') else None,
            'turn_rate': float(match.group('turn_rate')) if match.group('turn_rate') else None,
            'flightlevel': float(match.group('flight_level')) if match.group('flight_level') else None,
            'signal_quality': float(match.group('signal_quality')) if match.group('signal_quality') else None,
            'error_count': int(match.group('errors')) if match.group('errors') else None,
            'frequency_offset': float(match.group('frequency_offset')) if match.group('frequency_offset') else None,
            'gps_status': match.group('gps_accuracy') if match.group('gps_accuracy') else None,
            'software_version': float(match.group('flarm_software_version')) if match.group('flarm_software_version') else None,
            'hardware_version': int(match.group('flarm_hardware_version'), 16) if match.group('flarm_hardware_version') else None}


def parse_status(aprs_comment):
    match = re.search(PATTERN_TRACKER_BEACON_STATUS, aprs_comment)
    return {'hardware_version': int(match.group('hardware_version')) if match.group('hardware_version') else None,
            'software_version': int(match.group('software_version')) if match.group('software_version') else None,
            'gps_satellites': int(match.group('gps_satellites')) if match.group('gps_satellites') else None,
            'gps_quality': int(match.group('gps_quality')) if match.group('gps_quality') else None,
            'gps_altitude': int(match.group('gps_altitude')) if match.group('gps_altitude') else None,
            'pressure': float(match.group('pressure')) if match.group('pressure') else None,
            'temperature': float(match.group('temperature')) if match.group('temperature') else None,
            'humidity': int(match.group('humidity')) if match.group('humidity') else None,
            'voltage': float(match.group('voltage')) if match.group('voltage') else None,
            'transmitter_power': int(match.group('transmitter_power')) if match.group('transmitter_power') else None,
            'noise_level': float(match.group('noise_level')) if match.group('noise_level') else None,
            'relays': int(match.group('relays')) if match.group('relays') else None}
