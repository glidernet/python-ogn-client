import unittest

from ogn.parser.parse import parse_ogn_receiver_beacon


class TestStringMethods(unittest.TestCase):
    def test_fail_validation(self):
        self.assertEqual(parse_ogn_receiver_beacon("notAValidToken"), None)

    def test_v021(self):
        receiver_beacon = parse_ogn_receiver_beacon("v0.2.1 CPU:0.8 RAM:25.6/458.9MB NTP:0.0ms/+0.0ppm +51.9C RF:+26-1.4ppm/-0.25dB")
        self.assertEqual(receiver_beacon['rec_crystal_correction'], 26)
        self.assertEqual(receiver_beacon['rec_crystal_correction_fine'], -1.4)
        self.assertEqual(receiver_beacon['rec_input_noise'], -0.25)

    def test_v022(self):
        receiver_beacon = parse_ogn_receiver_beacon("v0.2.2.x86 CPU:0.5 RAM:669.9/887.7MB NTP:1.0ms/+6.2ppm +52.0C RF:+0.06dB")
        self.assertEqual(receiver_beacon['version'], '0.2.2')
        self.assertEqual(receiver_beacon['platform'], 'x86')
        self.assertEqual(receiver_beacon['cpu_load'], 0.5)
        self.assertEqual(receiver_beacon['cpu_temp'], 52.0)
        self.assertEqual(receiver_beacon['free_ram'], 669.9)
        self.assertEqual(receiver_beacon['total_ram'], 887.7)
        self.assertEqual(receiver_beacon['ntp_error'], 1.0)
        self.assertEqual(receiver_beacon['rec_crystal_correction'], 0.0)
        self.assertEqual(receiver_beacon['rec_crystal_correction_fine'], 0.0)
        self.assertEqual(receiver_beacon['rec_input_noise'], 0.06)

    def test_v025(self):
        receiver_beacon = parse_ogn_receiver_beacon("v0.2.5.RPI-GPU CPU:0.8 RAM:287.3/458.7MB NTP:1.0ms/-6.4ppm 5.016V 0.534A +51.9C RF:+55+0.4ppm/-0.67dB/+10.8dB@10km[57282]")
        self.assertEqual(receiver_beacon['voltage'], 5.016)
        self.assertEqual(receiver_beacon['amperage'], 0.534)
        self.assertEqual(receiver_beacon['senders_signal'], 10.8)
        self.assertEqual(receiver_beacon['senders_messages'], 57282)

        receiver_beacon = parse_ogn_receiver_beacon("v0.2.5.ARM CPU:0.4 RAM:638.0/970.5MB NTP:0.2ms/-1.1ppm +65.5C 14/16Acfts[1h] RF:+45+0.0ppm/+3.88dB/+24.0dB@10km[143717]/+26.7dB@10km[68/135]")
        self.assertEqual(receiver_beacon['senders_visible'], 14)
        self.assertEqual(receiver_beacon['senders_total'], 16)
        self.assertEqual(receiver_beacon['senders_signal'], 24.0)
        self.assertEqual(receiver_beacon['senders_messages'], 143717)
        self.assertEqual(receiver_beacon['good_senders_signal'], 26.7)
        self.assertEqual(receiver_beacon['good_senders'], 68)
        self.assertEqual(receiver_beacon['good_and_bad_senders'], 135)


if __name__ == '__main__':
    unittest.main()
