from ogn.parser.pattern import PATTERN_TRACKER_POSITION_COMMENT, PATTERN_TRACKER_STATUS_COMMENT
from ogn.parser.utils import FPM_TO_MS, HPM_TO_DEGS

from .base import BaseParser


class TrackerParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'tracker'
        self.position_pattern = PATTERN_TRACKER_POSITION_COMMENT
        self.status_pattern = PATTERN_TRACKER_STATUS_COMMENT

    def parse_position(self, aprs_comment):
        match = self.position_pattern.match(aprs_comment)

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
        if match.group('error_count'): result['error_count'] = int(match.group('error_count'))
        if match.group('frequency_offset'): result['frequency_offset'] = float(match.group('frequency_offset'))
        if match.group('gps_quality'):
            result.update({
                'gps_quality': {
                    'horizontal': int(match.group('gps_quality_horizontal')),
                    'vertical': int(match.group('gps_quality_vertical'))
                }
            })
        if match.group('signal_power'): result['signal_power'] = float(match.group('signal_power'))
        return result

    def parse_status(self, aprs_comment):
        match = self.status_pattern.match(aprs_comment)
        if match:
            result = {}

            if match.group('hardware_version'): result['hardware_version'] = int(match.group('hardware_version'))
            if match.group('software_version'): result['software_version'] = int(match.group('software_version'))
            if match.group('gps_satellites'): result['gps_satellites'] = int(match.group('gps_satellites'))
            if match.group('gps_quality'): result['gps_quality'] = int(match.group('gps_quality'))
            if match.group('gps_altitude'): result['gps_altitude'] = int(match.group('gps_altitude'))
            if match.group('pressure'): result['pressure'] = float(match.group('pressure'))
            if match.group('temperature'): result['temperature'] = float(match.group('temperature'))
            if match.group('humidity'): result['humidity'] = int(match.group('humidity'))
            if match.group('voltage'): result['voltage'] = float(match.group('voltage'))
            if match.group('transmitter_power'): result['transmitter_power'] = int(match.group('transmitter_power'))
            if match.group('noise_level'): result['noise_level'] = float(match.group('noise_level'))
            if match.group('relays'): result['relays'] = int(match.group('relays'))
            return result
        else:
            return {'comment': aprs_comment}
