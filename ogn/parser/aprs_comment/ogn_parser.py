import re

from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS
from ogn.parser.pattern import PATTERN_RECEIVER_BEACON, PATTERN_AIRCRAFT_BEACON

from .base import BaseParser


class OgnParser(BaseParser):
    def __init__(self):
        self.beacon_type = None
        self.aircraft_pattern = re.compile(PATTERN_AIRCRAFT_BEACON)
        self.receiver_pattern = re.compile(PATTERN_RECEIVER_BEACON)

    def parse(self, aprs_comment, aprs_type):
        if not aprs_comment:
            return {'beacon_type': 'aprs_receiver'}

        ac_data = self.parse_aircraft_beacon(aprs_comment)
        if ac_data:
            ac_data.update({'beacon_type': 'aprs_aircraft'})
            return ac_data

        rc_data = self.parse_receiver_beacon(aprs_comment)
        if rc_data:
            rc_data.update({'beacon_type': 'aprs_receiver'})
            return rc_data
        else:
            return {'user_comment': aprs_comment,
                    'beacon_type': 'aprs_receiver'}

    def parse_aircraft_beacon(self, aprs_comment):
        ac_match = self.aircraft_pattern.match(aprs_comment)
        if ac_match:
            return {'address_type': int(ac_match.group('details'), 16) & 0b00000011,
                    'aircraft_type': (int(ac_match.group('details'), 16) & 0b01111100) >> 2,
                    'stealth': (int(ac_match.group('details'), 16) & 0b10000000) >> 7 == 1,
                    'address': ac_match.group('address'),
                    'climb_rate': int(ac_match.group('climb_rate')) * FPM_TO_MS if ac_match.group('climb_rate') else None,
                    'turn_rate': float(ac_match.group('turn_rate')) * HPM_TO_DEGS if ac_match.group('turn_rate') else None,
                    'flightlevel': float(ac_match.group('flight_level')) if ac_match.group('flight_level') else None,
                    'signal_quality': float(ac_match.group('signal_quality')) if ac_match.group('signal_quality') else None,
                    'error_count': int(ac_match.group('errors')) if ac_match.group('errors') else None,
                    'frequency_offset': float(ac_match.group('frequency_offset')) if ac_match.group('frequency_offset') else None,
                    'gps_quality': {'horizontal': int(ac_match.group('gps_quality_horizontal')),
                                    'vertical': int(ac_match.group('gps_quality_vertical'))} if ac_match.group('gps_quality') else None,
                    'software_version': float(ac_match.group('flarm_software_version')) if ac_match.group('flarm_software_version') else None,
                    'hardware_version': int(ac_match.group('flarm_hardware_version'), 16) if ac_match.group('flarm_hardware_version') else None,
                    'real_address': ac_match.group('flarm_id') if ac_match.group('flarm_id') else None,
                    'signal_power': float(ac_match.group('signal_power')) if ac_match.group('signal_power') else None,
                    'proximity': [hear[4:] for hear in ac_match.group('proximity').split(" ")] if ac_match.group('proximity') else None}
        else:
            return None

    def parse_receiver_beacon(self, aprs_comment):
        rec_match = self.receiver_pattern.match(aprs_comment)
        if rec_match:
            return {'version': rec_match.group('version'),
                    'platform': rec_match.group('platform'),
                    'cpu_load': float(rec_match.group('cpu_load')),
                    'free_ram': float(rec_match.group('ram_free')),
                    'total_ram': float(rec_match.group('ram_total')),
                    'ntp_error': float(rec_match.group('ntp_offset')),
                    'rt_crystal_correction': float(rec_match.group('ntp_correction')),
                    'voltage': float(rec_match.group('voltage')) if rec_match.group('voltage') else None,
                    'amperage': float(rec_match.group('amperage')) if rec_match.group('amperage') else None,
                    'cpu_temp': float(rec_match.group('cpu_temperature')) if rec_match.group('cpu_temperature') else None,
                    'senders_visible': int(rec_match.group('visible_senders')) if rec_match.group('visible_senders') else None,
                    'senders_total': int(rec_match.group('senders')) if rec_match.group('senders') else None,
                    'rec_crystal_correction': int(rec_match.group('rf_correction_manual')) if rec_match.group('rf_correction_manual') else None,
                    'rec_crystal_correction_fine': float(rec_match.group('rf_correction_automatic')) if rec_match.group('rf_correction_automatic') else None,
                    'rec_input_noise': float(rec_match.group('signal_quality')) if rec_match.group('signal_quality') else None,
                    'senders_signal': float(rec_match.group('senders_signal_quality')) if rec_match.group('senders_signal_quality') else None,
                    'senders_messages': float(rec_match.group('senders_messages')) if rec_match.group('senders_messages') else None,
                    'good_senders_signal': float(rec_match.group('good_senders_signal_quality')) if rec_match.group('good_senders_signal_quality') else None,
                    'good_senders': float(rec_match.group('good_senders')) if rec_match.group('good_senders') else None,
                    'good_and_bad_senders': float(rec_match.group('good_and_bad_senders')) if rec_match.group('good_and_bad_senders') else None}
        else:
            return None
