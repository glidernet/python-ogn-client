import unittest

from ogn.parser.aprs_comment.receiver_parser import ReceiverParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = ReceiverParser().parse_position("Antenna: chinese, on a pylon, 20 meter above ground")

        assert message['user_comment'] == "Antenna: chinese, on a pylon, 20 meter above ground"

    def test_position_comment_empty(self):
        message = ReceiverParser().parse_position("")

        self.assertIsNotNone(message)

    def test_status_comment(self):
        message = ReceiverParser().parse_status("v0.2.7.RPI-GPU CPU:0.7 RAM:770.2/968.2MB NTP:1.8ms/-3.3ppm +55.7C 7/8Acfts[1h] RF:+54-1.1ppm/-0.16dB/+7.1dB@10km[19481]/+16.8dB@10km[7/13]")

        assert message['version'] == "0.2.7"
        assert message['platform'] == 'RPI-GPU'
        assert message['cpu_load'] == 0.7
        assert message['free_ram'] == 770.2
        assert message['total_ram'] == 968.2
        assert message['ntp_error'] == 1.8
        assert message['rt_crystal_correction'] == -3.3
        assert message['cpu_temp'] == 55.7
        assert message['senders_visible'] == 7
        assert message['senders_total'] == 8
        assert message['rec_crystal_correction'] == 54
        assert message['rec_crystal_correction_fine'] == -1.1
        assert message['rec_input_noise'] == -0.16
        assert message['senders_signal'] == 7.1
        assert message['senders_messages'] == 19481
        assert message['good_senders_signal'] == 16.8
        assert message['good_senders'] == 7
        assert message['good_and_bad_senders'] == 13


if __name__ == '__main__':
    unittest.main()
