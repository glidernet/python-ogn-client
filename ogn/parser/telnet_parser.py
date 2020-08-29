from datetime import datetime

from ogn.parser.utils import createTimestamp
from ogn.parser.pattern import PATTERN_TELNET_50001

telnet_50001_pattern = PATTERN_TELNET_50001


def parse(telnet_data):
    reference_timestamp = datetime.utcnow()

    match = telnet_50001_pattern.match(telnet_data)
    if match:
        return {'pps_offset': float(match.group('pps_offset')),
                'frequency': float(match.group('frequency')),
                'aircraft_type': int(match.group('aircraft_type')),
                'address_type': int(match.group('address_type')),
                'address': match.group('address'),
                'timestamp': createTimestamp(match.group('timestamp') + 'h', reference_timestamp),
                'latitude': float(match.group('latitude')),
                'longitude': float(match.group('longitude')),
                'altitude': int(match.group('altitude')),
                'climb_rate': float(match.group('climb_rate')),
                'ground_speed': float(match.group('ground_speed')),
                'track': float(match.group('track')),
                'turn_rate': float(match.group('turn_rate')),
                'magic_number': int(match.group('magic_number')),
                'gps_status': match.group('gps_status'),
                'channel': int(match.group('channel')),
                'flarm_timeslot': match.group('flarm_timeslot') == 'f',
                'ogn_timeslot': match.group('ogn_timeslot') == 'o',
                'frequency_offset': float(match.group('frequency_offset')),
                'decode_quality': float(match.group('decode_quality')),
                'signal_quality': float(match.group('signal_quality')),
                'demodulator_type': int(match.group('demodulator_type')),
                'error_count': float(match.group('error_count')),
                'distance': float(match.group('distance')),
                'bearing': float(match.group('bearing')),
                'phi': float(match.group('phi')),
                'multichannel': match.group('multichannel') == '+'}
    else:
        return None
