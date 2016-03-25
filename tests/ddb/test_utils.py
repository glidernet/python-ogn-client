import unittest

from ogn.ddb import get_ddb_devices


class TestStringMethods(unittest.TestCase):
    def test_get_ddb_devices(self):
        devices = list(get_ddb_devices())
        self.assertGreater(len(devices), 4000)
        self.assertCountEqual(devices[0].keys(), ['device_type', 'device_id', 'aircraft_model', 'registration', 'cn', 'tracked', 'identified'])
