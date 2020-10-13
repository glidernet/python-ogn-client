import unittest

from datetime import datetime

from ogn.parser.utils import KNOTS_TO_MS, KPH_TO_MS, FEETS_TO_METER, fahrenheit_to_celsius
from ogn.parser.parse import parse_aprs
from ogn.parser.exceptions import AprsParseError


class TestStringMethods(unittest.TestCase):
    def test_fail_validation(self):
        with self.assertRaises(AprsParseError):
            parse_aprs("notAValidString")

    def test_basic(self):
        message = parse_aprs("FLRDDA5BA>APRS,qAS,LFMX:/160829h4415.41N/00600.03E'342/049/A=005524 this is a comment")

        self.assertEqual(message['aprs_type'], 'position')
        self.assertEqual(message['name'], "FLRDDA5BA")
        self.assertEqual(message['dstcall'], "APRS")
        self.assertEqual(message['receiver_name'], "LFMX")
        self.assertEqual(message['timestamp'].strftime('%H:%M:%S'), "16:08:29")
        self.assertAlmostEqual(message['latitude'], 44.25683, 5)
        self.assertEqual(message['symboltable'], '/')
        self.assertAlmostEqual(message['longitude'], 6.0005, 5)
        self.assertEqual(message['symbolcode'], '\'')
        self.assertEqual(message['track'], 342)
        self.assertEqual(message['ground_speed'], 49 * KNOTS_TO_MS / KPH_TO_MS)
        self.assertAlmostEqual(message['altitude'], 5524 * FEETS_TO_METER, 5)
        self.assertEqual(message['comment'], "this is a comment")

    def test_v024(self):
        # higher precision datum format introduced
        raw_message = "FLRDDA5BA>APRS,qAS,LFMX:/160829h4415.41N/00600.03E'342/049/A=005524 !W26! id21400EA9 -2454fpm +0.9rot 19.5dB 0e -6.6kHz gps1x1 s6.02 h44 rDF0C56"
        message = parse_aprs(raw_message)

        self.assertEqual(message['aprs_type'], 'position')
        self.assertAlmostEqual(message['latitude'] - 44.2568 - 1 / 30000, 2 / 1000 / 60, 10)
        self.assertAlmostEqual(message['longitude'] - 6.0005, 6 / 1000 / 60, 10)

    def test_v025(self):
        # introduced the "aprs status" format where many informations (lat, lon, alt, speed, ...) are just optional
        raw_message = "EPZR>APRS,TCPIP*,qAC,GLIDERN1:>093456h this is a comment"
        message = parse_aprs(raw_message)

        self.assertEqual(message['aprs_type'], 'status')
        self.assertEqual(message['name'], "EPZR")
        self.assertEqual(message['receiver_name'], "GLIDERN1")
        self.assertEqual(message['timestamp'].strftime('%H:%M:%S'), "09:34:56")
        self.assertEqual(message['comment'], "this is a comment")

    def test_v026(self):
        # from 0.2.6 the ogn comment of a receiver beacon is just optional
        raw_message = "Ulrichamn>APRS,TCPIP*,qAC,GLIDERN1:/085616h5747.30NI01324.77E&/A=001322"
        message = parse_aprs(raw_message)

        self.assertEqual(message['aprs_type'], 'position')
        self.assertEqual(message['comment'], '')

    def test_v026_relay(self):
        # beacons can be relayed
        raw_message = "FLRFFFFFF>OGNAVI,NAV07220E*,qAS,NAVITER:/092002h1000.00S/01000.00W'000/000/A=003281 !W00! id2820FFFFFF +300fpm +1.7rot"
        message = parse_aprs(raw_message)

        self.assertEqual(message['aprs_type'], 'position')
        self.assertEqual(message['relay'], "NAV07220E")

    def test_v027_ddhhmm(self):
        # beacons can have hhmmss or ddhhmm timestamp
        raw_message = "ICA4B0678>APRS,qAS,LSZF:/301046z4729.50N/00812.89E'227/091/A=002854 !W01! id054B0678 +040fpm +0.0rot 19.0dB 0e +1.5kHz gps1x1"
        message = parse_aprs(raw_message)

        self.assertEqual(message['aprs_type'], 'position')
        self.assertEqual(message['timestamp'].strftime('%d %H:%M'), "30 10:46")

    def test_v028_fanet_position_weather(self):
        # with v0.2.8 fanet devices can report weather data
        raw_message = 'FNTFC9002>OGNFNT,qAS,LSXI2:/163051h4640.33N/00752.21E_187/004g007t075h78b63620 29.0dB -8.0kHz'
        message = parse_aprs(raw_message)

        self.assertEqual(message['aprs_type'], 'position_weather')
        self.assertEqual(message['wind_direction'], 187)
        self.assertEqual(message['wind_speed'], 4 * KNOTS_TO_MS / KPH_TO_MS)
        self.assertEqual(message['wind_speed_peak'], 7 * KNOTS_TO_MS / KPH_TO_MS)
        self.assertEqual(message['temperature'], fahrenheit_to_celsius(75))
        self.assertEqual(message['humidity'], 78 * 0.01)
        self.assertEqual(message['barometric_pressure'], 63620)

        self.assertEqual(message['comment'], '29.0dB -8.0kHz')

    def test_v028_fanet_position_weather_empty(self):
        raw_message = 'FNT010115>OGNFNT,qAS,DB7MJ:/065738h4727.72N/01012.83E_.../...g...t... 27.8dB -13.8kHz'
        message = parse_aprs(raw_message)

        self.assertEqual(message['aprs_type'], 'position_weather')
        self.assertIsNone(message['wind_direction'])
        self.assertIsNone(message['wind_speed'])
        self.assertIsNone(message['wind_speed_peak'])
        self.assertIsNone(message['temperature'])
        self.assertIsNone(message['humidity'])
        self.assertIsNone(message['barometric_pressure'])

    def test_negative_altitude(self):
        # some devices can report negative altitudes
        raw_message = "OGNF71F40>APRS,qAS,NAVITER:/080852h4414.37N/01532.06E'253/052/A=-00013 !W73! id1EF71F40 -060fpm +0.0rot"
        message = parse_aprs(raw_message)

        self.assertAlmostEqual(message['altitude'], -13 * FEETS_TO_METER, 5)

    def test_no_altitude(self):
        # altitude is not a 'must have'
        raw_message = "FLRDDEEF1>OGCAPT,qAS,CAPTURS:/065511h4837.63N/00233.79E'000/000"
        message = parse_aprs(raw_message)

        self.assertEqual(message['altitude'], None)

    def test_invalid_coordinates(self):
        # sometimes the coordinates leave their valid range: -90<=latitude<=90 or -180<=longitude<=180
        with self.assertRaises(AprsParseError):
            parse_aprs("RND000000>APRS,qAS,TROCALAN1:/210042h6505.31S/18136.75W^054/325/A=002591 !W31! idA4000000 +099fpm +1.8rot FL029.04 12.0dB 5e -6.3kHz gps11x17")

        with self.assertRaises(AprsParseError):
            parse_aprs("RND000000>APRS,qAS,TROCALAN1:/210042h9505.31S/17136.75W^054/325/A=002591 !W31! idA4000000 +099fpm +1.8rot FL029.04 12.0dB 5e -6.3kHz gps11x17")

    def test_invalid_timestamp(self):
        with self.assertRaises(AprsParseError):
            parse_aprs("OGND4362A>APRS,qAS,Eternoz:/194490h4700.25N/00601.47E'003/063/A=000000 !W22! id07D4362A 0fpm +0.0rot FL000.00 2.0dB 3e -2.8kHz gps3x4 +12.2dBm")

        with self.assertRaises(AprsParseError):
            parse_aprs("Ulrichamn>APRS,TCPIP*,qAC,GLIDERN1:/194490h5747.30NI01324.77E&/A=001322")

    def test_invalid_altitude(self):
        with self.assertRaises(AprsParseError):
            parse_aprs("Ulrichamn>APRS,TCPIP*,qAC,GLIDERN1:/085616h5747.30NI01324.77E&/A=12-345")

    def test_bad_comment(self):
        raw_message = "# bad configured ogn receiver"
        message = parse_aprs(raw_message)

        self.assertEqual(message['comment'], raw_message)
        self.assertEqual(message['aprs_type'], 'comment')

    def test_server_comment(self):
        raw_message = "# aprsc 2.1.4-g408ed49 17 Mar 2018 09:30:36 GMT GLIDERN1 37.187.40.234:10152"
        message = parse_aprs(raw_message)

        self.assertEqual(message['version'], '2.1.4-g408ed49')
        self.assertEqual(message['timestamp'], datetime(2018, 3, 17, 9, 30, 36))
        self.assertEqual(message['server'], 'GLIDERN1')
        self.assertEqual(message['ip_address'], '37.187.40.234')
        self.assertEqual(message['port'], '10152')
        self.assertEqual(message['aprs_type'], 'server')


if __name__ == '__main__':
    unittest.main()
