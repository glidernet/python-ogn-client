import re

from ogn.parser.pattern import PATTERN_RECEIVER_POSITION_COMMENT, PATTERN_RECEIVER_STATUS_COMMENT

from .base import BaseParser


class ReceiverParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'receiver'
        self.position_pattern = re.compile(PATTERN_RECEIVER_POSITION_COMMENT)
        self.status_pattern = re.compile(PATTERN_RECEIVER_STATUS_COMMENT)

    def parse_position(self, aprs_comment):
        if aprs_comment is None:
            return {}
        else:
            match = self.position_pattern.match(aprs_comment)
            return {'user_comment': match.group('user_comment') if match.group('user_comment') else None}

    def parse_status(self, aprs_comment):
        match = self.status_pattern.match(aprs_comment)
        return {'version': match.group('version'),
                'platform': match.group('platform'),
                'cpu_load': float(match.group('cpu_load')),
                'free_ram': float(match.group('ram_free')),
                'total_ram': float(match.group('ram_total')),
                'ntp_error': float(match.group('ntp_offset')),
                'rt_crystal_correction': float(match.group('ntp_correction')),
                'voltage': float(match.group('voltage')) if match.group('voltage') else None,
                'amperage': float(match.group('amperage')) if match.group('amperage') else None,
                'cpu_temp': float(match.group('cpu_temperature')) if match.group('cpu_temperature') else None,
                'senders_visible': int(match.group('visible_senders')) if match.group('visible_senders') else None,
                'senders_total': int(match.group('senders')) if match.group('senders') else None,
                'rec_crystal_correction': int(match.group('rf_correction_manual')) if match.group('rf_correction_manual') else None,
                'rec_crystal_correction_fine': float(match.group('rf_correction_automatic')) if match.group('rf_correction_automatic') else None,
                'rec_input_noise': float(match.group('signal_quality')) if match.group('signal_quality') else None,
                'senders_signal': float(match.group('senders_signal_quality')) if match.group('senders_signal_quality') else None,
                'senders_messages': float(match.group('senders_messages')) if match.group('senders_messages') else None,
                'good_senders_signal': float(match.group('good_senders_signal_quality')) if match.group('good_senders_signal_quality') else None,
                'good_senders': float(match.group('good_senders')) if match.group('good_senders') else None,
                'good_and_bad_senders': float(match.group('good_and_bad_senders')) if match.group('good_and_bad_senders') else None}
