import unittest.mock as mock
import pytest

from ogn.parser import parse
from ogn.client.client import create_aprs_login, AprsClient
from ogn.client.settings import APRS_APP_NAME, APRS_APP_VER, APRS_KEEPALIVE_TIME


def test_create_aprs_login():
    basic_login = create_aprs_login('klaus', -1, 'myApp', '0.1')
    assert 'user klaus pass -1 vers myApp 0.1\n' == basic_login

    login_with_filter = create_aprs_login('klaus', -1, 'myApp', '0.1', 'r/48.0/11.0/100')
    assert 'user klaus pass -1 vers myApp 0.1 filter r/48.0/11.0/100\n' == login_with_filter


def test_initialisation():
    client = AprsClient(aprs_user='testuser', aprs_filter='')
    assert client.aprs_user == 'testuser'
    assert client.aprs_filter == ''


@mock.patch('ogn.client.client.socket')
def test_connect_full_feed(mock_socket):
    client = AprsClient(aprs_user='testuser', aprs_filter='')
    client.connect()
    client.sock.send.assert_called_once_with(f'user testuser pass -1 vers {APRS_APP_NAME} {APRS_APP_VER}\n'.encode('ascii'))
    client.sock.makefile.assert_called_once_with('rb')


@mock.patch('ogn.client.client.socket')
def test_connect_client_defined_filter(mock_socket):
    client = AprsClient(aprs_user='testuser', aprs_filter='r/50.4976/9.9495/100')
    client.connect()
    client.sock.send.assert_called_once_with(f'user testuser pass -1 vers {APRS_APP_NAME} {APRS_APP_VER} filter r/50.4976/9.9495/100\n'.encode('ascii'))
    client.sock.makefile.assert_called_once_with('rb')


@mock.patch('ogn.client.client.socket')
def test_disconnect(mock_socket):
    client = AprsClient(aprs_user='testuser', aprs_filter='')
    client.connect()
    client.disconnect()
    client.sock.shutdown.assert_called_once_with(0)
    client.sock.close.assert_called_once_with()
    assert client._kill is True


@mock.patch('ogn.client.client.socket')
def test_run(mock_socket):
    import socket
    mock_socket.error = socket.error

    client = AprsClient(aprs_user='testuser', aprs_filter='')
    client.connect()

    client.sock_file.readline = mock.MagicMock()
    client.sock_file.readline.side_effect = [b'Normal text blabla',
                                             b'my weird character \xc2\xa5',
                                             UnicodeDecodeError('funnycodec', b'\x00\x00', 1, 2, 'This is just a fake reason!'),
                                             b'... show must go on',
                                             BrokenPipeError(),
                                             b'... and on',
                                             ConnectionResetError(),
                                             b'... and on',
                                             socket.error(),
                                             b'... and on',
                                             b'',
                                             b'... and on',
                                             KeyboardInterrupt()]

    try:
        client.run(callback=lambda msg: print("got: {}".format(msg)), autoreconnect=True)
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()


@mock.patch('ogn.client.client.time')
@mock.patch('ogn.client.client.socket')
def test_run_keepalive(mock_socket, mock_time):
    import socket
    mock_socket.error = socket.error

    client = AprsClient(aprs_user='testuser', aprs_filter='')
    client.connect()

    client.sock_file.readline = mock.MagicMock()
    client.sock_file.readline.side_effect = [b'Normal text blabla',
                                             KeyboardInterrupt()]

    mock_time.side_effect = [0, 0, APRS_KEEPALIVE_TIME + 1, APRS_KEEPALIVE_TIME + 1]

    timed_callback = mock.MagicMock()

    try:
        client.run(callback=lambda msg: print("got: {}".format(msg)), timed_callback=timed_callback)
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()

    timed_callback.assert_called_with(client)


def test_reset_kill_reconnect():
    client = AprsClient(aprs_user='testuser', aprs_filter='')
    client.connect()

    # .run() should be allowed to execute after .connect()
    mock_callback = mock.MagicMock(
        side_effect=lambda raw_msg: client.disconnect())

    assert client._kill is False
    client.run(callback=mock_callback, autoreconnect=True)

    # After .disconnect(), client._kill should be True
    assert client._kill is True
    assert mock_callback.call_count == 1

    # After we reconnect, .run() should be able to run again
    mock_callback.reset_mock()
    client.connect()
    client.run(callback=mock_callback, autoreconnect=True)
    assert mock_callback.call_count == 1


@pytest.mark.skip("Too much invalid APRS data on the live feed")
def test_50_live_messages():
    print("Enter")
    remaining_messages = 50

    def process_message(raw_message):
        global remaining_messages
        if raw_message[0] == '#':
            return
        try:
            message = parse(raw_message)
            print("{}: {}".format(message['aprs_type'], raw_message))
        except NotImplementedError as e:
            print("{}: {}".format(e, raw_message))
            return
        if remaining_messages > 0:
            remaining_messages -= 1
        else:
            raise KeyboardInterrupt

    client = AprsClient(aprs_user='testuser', aprs_filter='')
    client.connect()
    try:
        client.run(callback=process_message, autoreconnect=True)
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()
