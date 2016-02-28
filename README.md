# python-ogn-client

[![Build Status](https://travis-ci.org/glidernet/python-ogn-client.svg?branch=master)]
(https://travis-ci.org/glidernet/python-ogn-client)
[![Coverage Status](https://img.shields.io/coveralls/glidernet/python-ogn-client.svg)]
(https://coveralls.io/r/glidernet/python-ogn-client)

A python3 module for the [Open Glider Network](http://wiki.glidernet.org/).
It can be used to connect to the OGN-APRS-Servers and to parse APRS-/OGN-Messages.

A full featured gateway with build-in database is provided by [py-ogn-gateway](https://github.com/glidernet/ogn-python).


## Example Usage

Parse APRS/OGN packet.

```
from ogn.parser import parse_aprs, parse_beacon
from datetime import datetime

beacon = parse_aprs("FLRDDDEAD>APRS,qAS,EDER:/114500h5029.86N/00956.98E'342/049/A=005524 id0ADDDEAD -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5",
                    reference_date=datetime(2016,1,1,11,46))
```

Connect to OGN and display all incoming beacons.

```
from ogn.client import ognClient
from ogn.parser import parse_aprs, parse_beacon, ParseError

def process_beacon(raw_message):
    if raw_message[0] == '#':
        print('Server Status: {}'.format(raw_message))
        return

    try:
        message = parse_aprs(raw_message)
        message.update(parse_beacon(message['comment']))

        print('Received {beacon_type} from {name}'.format(**message))
    except ParseError as e:
        print('Error, {}'.format(e.message))

client = ognClient(aprs_user='N0CALL')
client.connect()

try:
    client.run(callback=process_beacon, autoreconnect=True)
except KeyboardInterrupt:
    print('\nStop ogn gateway')
    client.disconnect()
```

## License
Licensed under the [AGPLv3](LICENSE).
