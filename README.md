# python-ogn-client

[![Build Status](https://travis-ci.org/glidernet/python-ogn-client.svg?branch=master)]
(https://travis-ci.org/glidernet/python-ogn-client)
[![PyPi Version](https://img.shields.io/pypi/v/ogn-client.svg)]
(https://pypi.python.org/pypi/ogn-client)
[![Coverage Status](https://coveralls.io/repos/github/glidernet/python-ogn-client/badge.svg?branch=master)]
(https://coveralls.io/github/glidernet/python-ogn-client?branch=master)

A python3 module for the [Open Glider Network](http://wiki.glidernet.org/).
It can be used to connect to the OGN-APRS-Servers and to parse APRS-/OGN-Messages.

A full featured gateway with build-in database is provided by [ogn-python](https://github.com/glidernet/ogn-python).


## Example Usage

Parse APRS/OGN packet.

```
from ogn.parser import parse_aprs, parse_ogn_beacon
from datetime import datetime

beacon = parse_aprs("FLRDDDEAD>OGN,qAS,EDER:/114500h5029.86N/00956.98E'342/049/A=005524 id0ADDDEAD -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5",
                    reference_date=datetime(2016,1,1,11,46))
beacon.update(parse_ogn_beacon(beacon['comment']))
```

Connect to OGN and display all incoming beacons.

```
from ogn.client import AprsClient
from ogn.parser import parse_aprs, parse_ogn_beacon, ParseError

def process_beacon(raw_message):
    if raw_message[0] == '#':
        print('Server Status: {}'.format(raw_message))
        return

    try:
        beacon = parse_aprs(raw_message)
        beacon.update(parse_ogn_beacon(beacon['comment']))

        print('Received {beacon_type} from {name}'.format(**beacon))
    except ParseError as e:
        print('Error, {}'.format(e.message))

client = AprsClient(aprs_user='N0CALL')
client.connect()

try:
    client.run(callback=process_beacon, autoreconnect=True)
except KeyboardInterrupt:
    print('\nStop ogn gateway')
    client.disconnect()
```

## License
Licensed under the [AGPLv3](LICENSE).
