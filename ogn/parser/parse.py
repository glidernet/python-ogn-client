from datetime import datetime, timezone

from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS, createTimestamp, KNOTS_TO_MS, KPH_TO_MS, FEETS_TO_METER, INCH_TO_MM, fahrenheit_to_celsius, CheapRuler, normalized_quality
from ogn.parser.exceptions import AprsParseError

from ogn_parser import parse as rust_parse

positions = {}
server_timestamp = None

dstcall_beacontype_mapping = {
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


def parse(aprs_message, reference_timestamp=None, calculate_relations=False, use_server_timestamp=True):
    global server_timestamp

    if use_server_timestamp is True:
        reference_timestamp = server_timestamp or datetime.now(timezone.utc)
    elif reference_timestamp is None:
        reference_timestamp = datetime.now(timezone.utc)

    rust_messages = rust_parse(aprs_message)
    if rust_messages:
        rust_message = rust_messages[0]
    else:
        raise AprsParseError("Empty message")

    message = {'raw_message': aprs_message, 'reference_timestamp': reference_timestamp}
    if parser_error := rust_message.get('parser_error'):
        raise AprsParseError(f"Parser error: {parser_error}")
    elif aprs_packet := rust_message.get('aprs_packet'):
        message.update({
            'aprs_type': 'position',
            'beacon_type': dstcall_beacontype_mapping.get(aprs_packet['to'], 'unknown'),
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
            if 'turn_rate' in position: message["turn_rate"] = float(position['turn_rate']) * HPM_TO_DEGS
            if 'signal_quality' in position: message["signal_quality"] = float(position['signal_quality'])
            if 'error' in position: message["error_count"] = position['error']
            if 'frequency_offset' in position: message["frequency_offset"] = float(position['frequency_offset'])
            if 'gps_quality' in position: message["gps_quality"] = position['gps_quality']
            if 'flight_level' in position: message["flightlevel"] = position['flight_level']
            if 'signal_power' in position: message["signal_power"] = position['signal_power']
            if 'software_version' in position: message["software_version"] = float(position['software_version'])
            if 'hardware_version' in position: message["hardware_version"] = position['hardware_version']
            if 'original_address' in position: message["real_address"] = f"{position['original_address']:06X}"

            if 'unparsed' in position: message["user_comment"] = position['unparsed']

        elif status := aprs_packet.get('status'):
            message['aprs_type'] = 'status'
            if 'timestamp' in status: message['timestamp'] = createTimestamp(status['timestamp'], reference_timestamp)

            if 'version' in status: message["version"] = status['version']
            if 'platform' in status: message["platform"] = status['platform']
            if 'cpu_load' in status: message["cpu_load"] = float(status['cpu_load'])
            if 'ram_free' in status: message["free_ram"] = float(status['ram_free'])
            if 'ram_total' in status: message["total_ram"] = float(status['ram_total'])
            if 'ntp_offset' in status: message["ntp_error"] = float(status['ntp_offset'])
            if 'ntp_correction' in status: message["rt_crystal_correction"] = float(status['ntp_correction'])
            if 'voltage' in status: message["voltage"] = float(status['voltage'])
            if 'amperage' in status: message["amperage"] = float(status['amperage'])
            if 'cpu_temperature' in status: message["cpu_temp"] = float(status['cpu_temperature'])
            if 'visible_senders' in status: message["senders_visible"] = status['visible_senders']
            if 'latency' in status: message["latency"] = status['latency']
            if 'senders' in status: message["senders_total"] = status['senders']
            if 'rf_correction_manual' in status: message["rec_crystal_correction"] = status['rf_correction_manual']
            if 'rf_correction_automatic' in status: message["rec_crystal_correction_fine"] = float(status['rf_correction_automatic'])
            if 'noise' in status: message["rec_input_noise"] = float(status['noise'])
            if 'senders_signal_quality' in status: message["senders_signal"] = float(status['senders_signal_quality'])
            if 'senders_messages' in status: message["senders_messages"] = status['senders_messages']
            if 'good_senders_signal_quality' in status: message["good_senders_signal"] = float(status['good_senders_signal_quality'])
            if 'good_senders' in status: message["good_senders"] = status['good_senders']
            if 'good_and_bad_senders' in status: message["good_and_bad_senders"] = status['good_and_bad_senders']

            if 'unparsed' in status: message["user_comment"] = status['unparsed']
        else:
            raise ValueError("Raised unreachable exception")
    elif server_comment := rust_message.get('server_comment'):
        message.update({
            'version': server_comment['version'],
            # 'timestamp': datetime.fromisoformat(server_comment['timestamp']), # only available in python 3.11+
            'timestamp': datetime.strptime(server_comment['timestamp'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc),
            'server': server_comment['server'],
            'ip_address': server_comment['ip_address'],
            'port': server_comment['port'],
            'aprs_type': 'server'})
    elif comment := rust_message.get('comment'):
        message.update({
            'comment': comment['comment'],
            'aprs_type': 'comment'})
    else:
        raise ValueError("Raised unreachable exception")

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
