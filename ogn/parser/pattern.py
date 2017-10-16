import re


PATTERN_APRS_POSITION = re.compile(r"^(?P<callsign>.+?)>(?P<dstcall>[A-Z0-9]+),((?P<relay>[A-Za-z0-9]+)\*)?.*,(?P<receiver>.+?):/(?P<time>\d{6}(h|z))(?P<latitude>\d{4}\.\d{2})(?P<latitude_sign>N|S)(?P<symbol_table>.)(?P<longitude>\d{5}\.\d{2})(?P<longitude_sign>E|W)(?P<symbol>.)(?P<course_extension>(?P<course>\d{3})/(?P<ground_speed>\d{3}))?/A=(?P<altitude>[-\d]{6})(?P<pos_extension>\s!W((?P<latitude_enhancement>\d)(?P<longitude_enhancement>\d))!)?(?:\s(?P<comment>.*))?$")
PATTERN_APRS_STATUS = re.compile(r"^(?P<callsign>.+?)>(?P<dstcall>[A-Z0-9]+),.+,(?P<receiver>.+?):>(?P<time>\d{6}(h|z))\s(?P<comment>.*)$")

PATTERN_NAVITER_BEACON = re.compile("""
    id(?P<details>[\dA-F]{4})(?P<id>[\dA-F]{6})\s
    (?P<climb_rate>[+-]\d+)fpm\s
    (?P<turn_rate>[+-][\d.]+)rot
""", re.VERBOSE | re.MULTILINE)

PATTERN_TRACKER_BEACON_POSITION = re.compile("""
    id(?P<details>\w{2})(?P<id>\w{6}?)\s?
    (?:(?P<climb_rate>[+-]\d+?)fpm\s)?
    (?:(?P<turn_rate>[+-][\d.]+?)rot\s)?
    (?:FL(?P<flight_level>[\d.]+)\s)?
    (?:(?P<signal_quality>[\d.]+?)dB\s)?
    (?:(?P<errors>\d+)e\s)?
    (?:(?P<frequency_offset>[+-][\d.]+?)kHz\s?)?
    (?:gps(?P<gps_accuracy>\d+x\d+)\s?)?
    (?:s(?P<flarm_software_version>[\d.]+)\s?)?
    (?:h(?P<flarm_hardware_version>[\dA-F]{2})\s?)?
""", re.VERBOSE | re.MULTILINE)

PATTERN_TRACKER_BEACON_STATUS = re.compile("""
    h(?P<hardware_version>[\d]{2})\s
    v(?P<software_version>[\d]{2})\s
    (?P<gps_satellites>[\d]+)sat/(?P<gps_quality>\d)\s
    (?P<gps_altitude>\d+)m\s
    (?P<pressure>[\d.]+)hPa\s
    (?P<temperature>[+-][\d.]+)degC\s
    (?P<humidity>\d+)%\s
    (?P<voltage>[\d.]+)V\s
    (?P<transmitter_power>\d+)/(?P<noise_level>[+-][\d.]+)dBm\s
    (?P<relays>\d+)/min
""", re.VERBOSE | re.MULTILINE)

PATTERN_RECEIVER_POSITION = re.compile(r"""
    (?:(?P<user_comment>.+))?
""", re.VERBOSE | re.MULTILINE)

PATTERN_RECEIVER_STATUS = re.compile("""
    (?:
        v(?P<version>\d+\.\d+\.\d+)
        (?:\.(?P<platform>.+?))?
    \s)?
    CPU:(?P<cpu_load>[\d.]+)\s
    RAM:(?P<ram_free>[\d.]+)/(?P<ram_total>[\d.]+)MB\s
    NTP:(?P<ntp_offset>[\d.]+)ms/(?P<ntp_correction>[+-][\d.]+)ppm\s
    (?:(?P<voltage>[\d.]+)V\s)?
    (?:(?P<amperage>[\d.]+)A\s)?
    (?:(?P<cpu_temperature>[+-][\d.]+)C\s*)?
    (?:(?P<visible_senders>\d+)/(?P<senders>\d+)Acfts\[1h\]\s*)?
    (?:RF:
        (?:
            (?P<rf_correction_manual>[+-][\d]+)
            (?P<rf_correction_automatic>[+-][\d.]+)ppm/
        )?
        (?P<signal_quality>[+-][\d.]+)dB
        (?:/(?P<senders_signal_quality>[+-][\d.]+)dB@10km\[(?P<senders_messages>\d+)\])?
        (?:/(?P<good_senders_signal_quality>[+-][\d.]+)dB@10km\[(?P<good_senders>\d+)/(?P<good_and_bad_senders>\d+)\])?
    )?
""", re.VERBOSE | re.MULTILINE)


# The following regexp patterns are part of the ruby ogn-client.
# source: https://github.com/svoop/ogn_client-ruby

# The MIT License (MIT)
#
# Copyright (c) 2015-2017 Sven Schwyn
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

PATTERN_RECEIVER_BEACON = re.compile(r"""
    (?:
        v(?P<version>\d+\.\d+\.\d+)
        (?:\.(?P<platform>.+?))?
    \s)?
    CPU:(?P<cpu_load>[\d.]+)\s
    RAM:(?P<ram_free>[\d.]+)/(?P<ram_total>[\d.]+)MB\s
    NTP:(?P<ntp_offset>[\d.]+)ms/(?P<ntp_correction>[+-][\d.]+)ppm\s
    (?:(?P<voltage>[\d.]+)V\s)?
    (?:(?P<amperage>[\d.]+)A\s)?
    (?:(?P<cpu_temperature>[+-][\d.]+)C\s*)?
    (?:(?P<visible_senders>\d+)/(?P<senders>\d+)Acfts\[1h\]\s*)?
    (?:RF:
        (?:
            (?P<rf_correction_manual>[+-][\d]+)
            (?P<rf_correction_automatic>[+-][\d.]+)ppm/
        )?
        (?P<signal_quality>[+-][\d.]+)dB
        (?:/(?P<senders_signal_quality>[+-][\d.]+)dB@10km\[(?P<senders_messages>\d+)\])?
        (?:/(?P<good_senders_signal_quality>[+-][\d.]+)dB@10km\[(?P<good_senders>\d+)/(?P<good_and_bad_senders>\d+)\])?
    )?
""", re.VERBOSE | re.MULTILINE)


PATTERN_AIRCRAFT_BEACON = re.compile(r"""
    id(?P<details>\w{2})(?P<id>\w{6}?)\s?
    (?:(?P<climb_rate>[+-]\d+?)fpm\s)?
    (?:(?P<turn_rate>[+-][\d.]+?)rot\s)?
    (?:id(?P<deviceID>[\d.]+)\s)?
    (?:FL(?P<flight_level>[\d.]+)\s)?
    (?:(?P<signal_quality>[\d.]+?)dB\s)?
    (?:(?P<errors>\d+)e\s)?
    (?:(?P<frequency_offset>[+-][\d.]+?)kHz\s?)?
    (?:gps(?P<gps_accuracy>\d+x\d+)\s?)?
    (?:s(?P<flarm_software_version>[\d.]+)\s?)?
    (?:h(?P<flarm_hardware_version>[\dA-F]{2})\s?)?
    (?:r(?P<flarm_id>[\dA-F]+)\s?)?
    (?:(?P<signal_power>[+-][\d.]+)dBm\s?)?
    (?:(?P<proximity>(hear[\dA-F]{4}\s?)+))?
""", re.VERBOSE | re.MULTILINE)
