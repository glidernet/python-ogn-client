from ogn.parser import parse


def test_v025():
    # introduced the "aprs status" format where many informations (lat, lon, alt, speed, ...) are just optional
    raw_message = "EPZR>APRS,TCPIP*,qAC,GLIDERN1:>093456h this is a comment"
    message = parse(raw_message)

    assert message['aprs_type'] == 'status'
    assert message['beacon_type'] == 'unknown'

    assert message['name'] == "EPZR"
    assert message['receiver_name'] == "GLIDERN1"
    assert message['timestamp'].strftime('%H:%M:%S') == "09:34:56"
    assert message['user_comment'] == "this is a comment"


def test():
    raw_message = "EPZR>APRS,TCPIP*,qAC,GLIDERN1:>093456h v0.2.7.RPI-GPU CPU:0.7 RAM:770.2/968.2MB NTP:1.8ms/-3.3ppm +55.7C 7/8Acfts[1h] RF:+54-1.1ppm/-0.16dB/+7.1dB@10km[19481]/+16.8dB@10km[7/13]"
    message = parse(raw_message)

    assert message['aprs_type'] == 'status'
    assert message['beacon_type'] == 'unknown'

    assert message['name'] == "EPZR"
    assert message['receiver_name'] == "GLIDERN1"
    assert message['timestamp'].strftime('%H:%M:%S') == "09:34:56"
    assert message['version'] == "0.2.7"
    assert message['platform'] == "RPI-GPU"
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
