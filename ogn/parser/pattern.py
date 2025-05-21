import re


PATTERN_TELNET_50001 = re.compile(r"""
    (?P<pps_offset>\d\.\d+)sec:(?P<frequency>\d+\.\d+)MHz:\s+
    (?P<aircraft_type>\d):(?P<address_type>\d):(?P<address>[A-F0-9]{6})\s
    (?P<timestamp>\d{6}):\s
    \[\s*(?P<latitude>[+-]\d+\.\d+),\s*(?P<longitude>[+-]\d+\.\d+)\]deg\s*
    (?P<altitude>\d+)m\s*
    (?P<climb_rate>[+-]\d+\.\d+)m/s\s*
    (?P<ground_speed>\d+\.\d+)m/s\s*
    (?P<track>\d+\.\d+)deg\s*
    (?P<turn_rate>[+-]\d+\.\d+)deg/sec\s*
    (?P<magic_number>\d+)\s*
    (?P<gps_status>[0-9x]+)m\s*
    (?P<channel>\d+)(?P<flarm_timeslot>[f_])(?P<ogn_timeslot>[o_])\s*
    (?P<frequency_offset>[+-]\d+\.\d+)kHz\s*
    (?P<decode_quality>\d+\.\d+)/(?P<signal_quality>\d+\.\d+)dB/(?P<demodulator_type>\d+)\s+
    (?P<error_count>\d+)e\s*
    (?P<distance>\d+\.\d+)km\s*
    (?P<bearing>\d+\.\d+)deg\s*
    (?P<phi>[+-]\d+\.\d+)deg\s*
    (?P<multichannel>\+)?\s*
    \?\s*
    R?\s*
    (B(?P<baro_altitude>\d+))?
""", re.VERBOSE | re.MULTILINE)
