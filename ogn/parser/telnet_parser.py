from datetime import datetime

from ogn.parser import ParseError
from ogn.parser.utils import createTimestamp


def parse(telnet_data):
    reference_timestamp = datetime.utcnow()

    try:
        return {'pps_offset': float(telnet_data[0:5]),
                'frequency': float(telnet_data[9:16]),
                'aircraft_type': int(telnet_data[20:24]),
                'address_type': int(telnet_data[25]),
                'address': telnet_data[27:33],
                'timestamp': createTimestamp(telnet_data[34:40] + 'h', reference_timestamp),
                'latitude': float(telnet_data[43:53]),
                'longitude': float(telnet_data[54:64]),
                'altitude': int(telnet_data[68:73]),
                'climb_rate': float(telnet_data[74:80]),
                'ground_speed': float(telnet_data[83:89]),
                'track': float(telnet_data[92:98]),
                'turn_rate': float(telnet_data[101:107]),
                'magic_number': int(telnet_data[114:116]),
                'gps_status': telnet_data[117:122],
                'channel': int(telnet_data[124:126]),
                'flarm_timeslot': telnet_data[126] == 'f',
                'ogn_timeslot': telnet_data[127] == 'o',
                'frequency_offset': float(telnet_data[128:134]),
                'decode_quality': float(telnet_data[137:142]),
                'signal_quality': float(telnet_data[143:147]),
                'demodulator_type': int(telnet_data[150:151]),
                'error_count': float(telnet_data[151:154]),
                'distance': float(telnet_data[155:162]),
                'bearing': float(telnet_data[164:170]),
                'phi': float(telnet_data[173:179]),
                'multichannel': telnet_data[183] == '+'}

    except Exception:
        raise ParseError
