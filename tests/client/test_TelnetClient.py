import unittest
import unittest.mock as mock

from ogn.client.client import TelnetClient


class TelnetClientTest(unittest.TestCase):
    @mock.patch('ogn.client.client.socket')
    def test_connect(self, socket_mock):
        def callback(raw_message):
            pass

        client = TelnetClient()
        client.run(callback=callback)
