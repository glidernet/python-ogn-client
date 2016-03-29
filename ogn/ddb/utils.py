import requests

DDB_URL = "http://ddb.glidernet.org/download/?j=1"


def get_ddb_devices():
    r = requests.get(DDB_URL)
    for device in r.json()['devices']:
        device.update({'identified': device['identified'] == 'Y',
                       'tracked': device['tracked'] == 'Y'})
        yield device
