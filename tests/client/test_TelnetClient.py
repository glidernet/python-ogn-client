import unittest.mock as mock

from ogn.client.client import TelnetClient


@mock.patch('ogn.client.client.socket')
def test_connect_disconnect(socket_mock):
    client = TelnetClient()
    client.connect()
    client.sock.connect.assert_called_once_with(('localhost', 50001))

    client.disconnect()
    client.sock.shutdown.assert_called_once_with(0)
    client.sock.close.assert_called_once_with()


@mock.patch('ogn.client.client.socket')
def test_run(socket_mock):
    def callback(raw_message):
        raise ConnectionRefusedError

    client = TelnetClient()
    client.connect()

    client.run(callback=callback)
