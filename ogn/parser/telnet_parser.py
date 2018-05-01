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
                'frequency_offset': float(telnet_data[123:129]),
                'signal_quality': float(telnet_data[132:137]),
                'error_count': float(telnet_data[139:142]),
                'distance': float(telnet_data[143:150]),
                'bearing': float(telnet_data[152:158]),
                'phi': float(telnet_data[161:167])}
    except:
        raise ParseError
