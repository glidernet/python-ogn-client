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
        ab_match = self.aircraft_pattern.match(aprs_comment)
        if ab_match:
            return {'address_type': int(ab_match.group('details'), 16) & 0b00000011,
                    'aircraft_type': (int(ab_match.group('details'), 16) & 0b01111100) >> 2,
                    'stealth': (int(ab_match.group('details'), 16) & 0b10000000) >> 7 == 1,
                    'address': ab_match.group('address'),
                    'climb_rate': int(ab_match.group('climb_rate')) * FPM_TO_MS if ab_match.group('climb_rate') else None,
                    'turn_rate': float(ab_match.group('turn_rate')) * HPM_TO_DEGS if ab_match.group('turn_rate') else None,
                    'flightlevel': float(ab_match.group('flight_level')) if ab_match.group('flight_level') else None,
                    'signal_quality': float(ab_match.group('signal_quality')) if ab_match.group('signal_quality') else None,
                    'error_count': int(ab_match.group('errors')) if ab_match.group('errors') else None,
                    'frequency_offset': float(ab_match.group('frequency_offset')) if ab_match.group('frequency_offset') else None,
                    'gps_quality': {'horizontal': int(ab_match.group('gps_quality_horizontal')),
                                    'vertical': int(ab_match.group('gps_quality_vertical'))} if ab_match.group('gps_quality') else None,
                    'software_version': float(ab_match.group('flarm_software_version')) if ab_match.group('flarm_software_version') else None,
                    'hardware_version': int(ab_match.group('flarm_hardware_version'), 16) if ab_match.group('flarm_hardware_version') else None,
                    'real_address': ab_match.group('flarm_id') if ab_match.group('flarm_id') else None,
                    'signal_power': float(ab_match.group('signal_power')) if ab_match.group('signal_power') else None,
                    'proximity': [hear[4:] for hear in ab_match.group('proximity').split(" ")] if ab_match.group('proximity') else None}
        else:
            return None

    def parse_receiver_beacon(self, aprs_comment):
        rb_match = self.receiver_pattern.match(aprs_comment)
        if rb_match:
            return {'version': rb_match.group('version'),
                    'platform': rb_match.group('platform'),
                    'cpu_load': float(rb_match.group('cpu_load')),
                    'free_ram': float(rb_match.group('ram_free')),
                    'total_ram': float(rb_match.group('ram_total')),
                    'ntp_error': float(rb_match.group('ntp_offset')),
                    'rt_crystal_correction': float(rb_match.group('ntp_correction')),
                    'voltage': float(rb_match.group('voltage')) if rb_match.group('voltage') else None,
                    'amperage': float(rb_match.group('amperage')) if rb_match.group('amperage') else None,
                    'cpu_temp': float(rb_match.group('cpu_temperature')) if rb_match.group('cpu_temperature') else None,
                    'senders_visible': int(rb_match.group('visible_senders')) if rb_match.group('visible_senders') else None,
                    'senders_total': int(rb_match.group('senders')) if rb_match.group('senders') else None,
                    'rec_crystal_correction': int(rb_match.group('rf_correction_manual')) if rb_match.group('rf_correction_manual') else None,
                    'rec_crystal_correction_fine': float(rb_match.group('rf_correction_automatic')) if rb_match.group('rf_correction_automatic') else None,
                    'rec_input_noise': float(rb_match.group('signal_quality')) if rb_match.group('signal_quality') else None,
                    'senders_signal': float(rb_match.group('senders_signal_quality')) if rb_match.group('senders_signal_quality') else None,
                    'senders_messages': float(rb_match.group('senders_messages')) if rb_match.group('senders_messages') else None,
                    'good_senders_signal': float(rb_match.group('good_senders_signal_quality')) if rb_match.group('good_senders_signal_quality') else None,
                    'good_senders': float(rb_match.group('good_senders')) if rb_match.group('good_senders') else None,
                    'good_and_bad_senders': float(rb_match.group('good_and_bad_senders')) if rb_match.group('good_and_bad_senders') else None}
        else:
            return None
