from datetime import datetime, timezone

from ogn.parser import parse


def test_comment():
    raw_message = "# bad configured ogn receiver"
    message = parse(raw_message)

    assert message['comment'] == raw_message
    assert message['aprs_type'] == 'comment'


def test_server_comment():
    raw_message = "# aprsc 2.1.4-g408ed49 17 Mar 2018 09:30:36 GMT GLIDERN1 37.187.40.234:10152"
    message = parse(raw_message)

    assert message['version'] == '2.1.4-g408ed49'
    assert message['timestamp'] == datetime(2018, 3, 17, 9, 30, 36, tzinfo=timezone.utc)
    assert message['server'] == 'GLIDERN1'
    assert message['ip_address'] == '37.187.40.234'
    assert message['port'] == 10152
    assert message['aprs_type'] == 'server'
