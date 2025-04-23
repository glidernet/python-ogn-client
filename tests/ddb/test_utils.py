from ogn.ddb import get_ddb_devices


def test_get_ddb_devices():
    devices = list(get_ddb_devices())
    assert len(devices) > 4000
    assert len(devices[0].keys()), len(['device_type', 'device_id', 'aircraft_model', 'registration', 'cn', 'tracked', 'identified'])
