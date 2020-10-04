from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS
from ogn.parser.pattern import PATTERN_RECEIVER_BEACON, PATTERN_AIRCRAFT_BEACON

from .base import BaseParser


class OgnParser(BaseParser):
    def __init__(self):
        self.beacon_type = None
        self.aircraft_pattern = PATTERN_AIRCRAFT_BEACON
        self.receiver_pattern = PATTERN_RECEIVER_BEACON

    def parse(self, aprs_comment, aprs_type):
        if not aprs_comment:
            return {'beacon_type': 'aprs_receiver'}

        ab_data = self.parse_aircraft_beacon(aprs_comment)
        if ab_data:
            ab_data.update({'beacon_type': 'aprs_aircraft'})
            return ab_data

        rb_data = self.parse_receiver_beacon(aprs_comment)
        if rb_data:
            rb_data.update({'beacon_type': 'aprs_receiver'})
            return rb_data
        else:
            return {'user_comment': aprs_comment,
                    'beacon_type': 'aprs_receiver'}

    def parse_aircraft_beacon(self, aprs_comment):
        match = self.aircraft_pattern.match(aprs_comment)
        if match:
            result = {}
            if match.group('details'):
                result.update({
                    'address_type': int(match.group('details'), 16) & 0b00000011,
                    'aircraft_type': (int(match.group('details'), 16) & 0b01111100) >> 2,
                    'stealth': (int(match.group('details'), 16) & 0b10000000) >> 7 == 1,
                    'address': match.group('address'),
                })
            if match.group('climb_rate'): result['climb_rate'] = int(match.group('climb_rate')) * FPM_TO_MS
            if match.group('turn_rate'): result['turn_rate'] = float(match.group('turn_rate')) * HPM_TO_DEGS
            if match.group('flight_level'): result['flightlevel'] = float(match.group('flight_level'))
            if match.group('signal_quality'): result['signal_quality'] = float(match.group('signal_quality'))
            if match.group('errors'): result['error_count'] = int(match.group('errors'))
            if match.group('frequency_offset'): result['frequency_offset'] = float(match.group('frequency_offset'))
            if match.group('gps_quality'):
                result.update({
                    'gps_quality': {
                        'horizontal': int(match.group('gps_quality_horizontal')),
                        'vertical': int(match.group('gps_quality_vertical'))
                    }
                })
            if match.group('flarm_software_version'): result['software_version'] = float(match.group('flarm_software_version'))
            if match.group('flarm_hardware_version'): result['hardware_version'] = int(match.group('flarm_hardware_version'), 16)
            if match.group('flarm_id'): result['real_address'] = match.group('flarm_id')
            if match.group('signal_power'): result['signal_power'] = float(match.group('signal_power'))
            if match.group('proximity'): result['proximity'] = [hear[4:] for hear in match.group('proximity').split(' ')]
            return result
        else:
            return None

    def parse_receiver_beacon(self, aprs_comment):
        match = self.receiver_pattern.match(aprs_comment)
        if match:
            result = {
                'version': match.group('version'),
                'platform': match.group('platform'),
                'cpu_load': float(match.group('cpu_load')),
                'free_ram': float(match.group('ram_free')),
                'total_ram': float(match.group('ram_total')),
                'ntp_error': float(match.group('ntp_offset')),
                'rt_crystal_correction': float(match.group('ntp_correction'))
            }
            if match.group('voltage'): result['voltage'] = float(match.group('voltage'))
            if match.group('amperage'): result['amperage'] = float(match.group('amperage'))
            if match.group('cpu_temperature'): result['cpu_temp'] = float(match.group('cpu_temperature'))
            if match.group('visible_senders'): result['senders_visible'] = int(match.group('visible_senders'))
            if match.group('senders'): result['senders_total'] = int(match.group('senders'))
            if match.group('latency'): result['latency'] = float(match.group('latency'))
            if match.group('rf_correction_manual'): result['rec_crystal_correction'] = int(match.group('rf_correction_manual'))
            if match.group('rf_correction_automatic'): result['rec_crystal_correction_fine'] = float(match.group('rf_correction_automatic'))
            if match.group('signal_quality'): result['rec_input_noise'] = float(match.group('signal_quality'))
            if match.group('senders_signal_quality'): result['senders_signal'] = float(match.group('senders_signal_quality'))
            if match.group('senders_messages'): result['senders_messages'] = float(match.group('senders_messages'))
            if match.group('good_senders_signal_quality'): result['good_senders_signal'] = float(match.group('good_senders_signal_quality'))
            if match.group('good_senders'): result['good_senders'] = float(match.group('good_senders'))
            if match.group('good_and_bad_senders'): result['good_and_bad_senders'] = float(match.group('good_and_bad_senders'))
            return result
        else:
            return None
