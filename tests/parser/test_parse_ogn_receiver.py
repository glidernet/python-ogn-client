import unittest

from ogn.parser.aprs_comment.ogn_parser import OgnParser


class TestStringMethods(unittest.TestCase):
    def test_fail_validation(self):
        self.assertEqual(OgnParser().parse_receiver_beacon("notAValidToken"), None)

    def test_v021(self):
        message = OgnParser().parse_receiver_beacon("v0.2.1 CPU:0.8 RAM:25.6/458.9MB NTP:0.1ms/+2.3ppm +51.9C RF:+26-1.4ppm/-0.25dB")

        self.assertEqual(message['version'], "0.2.1")
        self.assertEqual(message['cpu_load'], 0.8)
        self.assertEqual(message['free_ram'], 25.6)
        self.assertEqual(message['total_ram'], 458.9)
        self.assertEqual(message['ntp_error'], 0.1)
        self.assertEqual(message['rt_crystal_correction'], 2.3)
        self.assertEqual(message['cpu_temp'], 51.9)

        self.assertEqual(message['rec_crystal_correction'], 26)
        self.assertEqual(message['rec_crystal_correction_fine'], -1.4)
        self.assertEqual(message['rec_input_noise'], -0.25)

    def test_v022(self):
        message = OgnParser().parse_receiver_beacon("v0.2.2.x86 CPU:0.5 RAM:669.9/887.7MB NTP:1.0ms/+6.2ppm +52.0C RF:+0.06dB")
        self.assertEqual(message['platform'], 'x86')

    def test_v025(self):
        message = OgnParser().parse_receiver_beacon("v0.2.5.RPI-GPU CPU:0.8 RAM:287.3/458.7MB NTP:1.0ms/-6.4ppm 5.016V 0.534A +51.9C RF:+55+0.4ppm/-0.67dB/+10.8dB@10km[57282]")
        self.assertEqual(message['voltage'], 5.016)
        self.assertEqual(message['amperage'], 0.534)
        self.assertEqual(message['senders_signal'], 10.8)
        self.assertEqual(message['senders_messages'], 57282)

        message = OgnParser().parse_receiver_beacon("v0.2.5.ARM CPU:0.4 RAM:638.0/970.5MB NTP:0.2ms/-1.1ppm +65.5C 14/16Acfts[1h] RF:+45+0.0ppm/+3.88dB/+24.0dB@10km[143717]/+26.7dB@10km[68/135]")
        self.assertEqual(message['senders_visible'], 14)
        self.assertEqual(message['senders_total'], 16)
        self.assertEqual(message['senders_signal'], 24.0)
        self.assertEqual(message['senders_messages'], 143717)
        self.assertEqual(message['good_senders_signal'], 26.7)
        self.assertEqual(message['good_senders'], 68)
        self.assertEqual(message['good_and_bad_senders'], 135)

    def test_v028(self):
        message = OgnParser().parse_receiver_beacon("v0.2.8.RPI-GPU CPU:0.3 RAM:744.5/968.2MB NTP:3.6ms/+2.0ppm +68.2C 3/3Acfts[1h] Lat:1.6s RF:-8+67.8ppm/+10.33dB/+1.3dB@10km[30998]/+10.4dB@10km[3/5]")
        self.assertEqual(message['latency'], 1.6)

    def test_relevant_keys_only(self):
        # return only keys where we got informations
        message = OgnParser().parse_receiver_beacon("v0.2.5.ARM CPU:0.4 RAM:638.0/970.5MB NTP:0.2ms/-1.1ppm")

        self.assertIsNotNone(message)
        self.assertEqual(sorted(message.keys()), sorted(['version', 'platform', 'cpu_load', 'free_ram', 'total_ram', 'ntp_error', 'rt_crystal_correction']))


if __name__ == '__main__':
    unittest.main()
