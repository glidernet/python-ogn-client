# python-ogn-client

[![build](https://github.com/Meisterschueler/python-ogn-client/actions/workflows/ci.yaml/badge.svg)](https://github.com/Meisterschueler/python-ogn-client/actions/workflows/ci.yaml)
[![PyPi Version](https://img.shields.io/pypi/v/ogn-client.svg)](https://pypi.python.org/pypi/ogn-client)

A python3 module for the [Open Glider Network](http://wiki.glidernet.org/).
It can be used to connect to the OGN-APRS-Servers and to parse APRS-/OGN-Messages.


## Installation

python-ogn-client is available at PyPI. So for installation simply use pip:

```
pip install ogn-client
```

## Example Usage

### Parse APRS/OGN packet.

```python
from ogn.parser import parse
from datetime import datetime

beacon = parse("FLRDDDEAD>APRS,qAS,EDER:/114500h5029.86N/00956.98E'342/049/A=005524 id0ADDDEAD -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5",
				reference_timestamp=datetime(2015, 7, 31, 12, 34, 56))
```

### Connect to OGN and display all incoming beacons.

```python
from ogn.client import AprsClient
from ogn.parser import parse, AprsParseError

def process_beacon(raw_message):
    try:
        beacon = parse(raw_message)
        print('Received {aprs_type}: {raw_message}'.format(**beacon))
    except AprsParseError as e:
        print('Error, {}'.format(e.message))

client = AprsClient(aprs_user='N0CALL')
client.connect()

try:
    client.run(callback=process_beacon, autoreconnect=True)
except KeyboardInterrupt:
    print('\nStop ogn gateway')
    client.disconnect()
```

### Connect to telnet console and display all decoded beacons.

```python
from ogn.client import TelnetClient
from ogn.parser.telnet_parser import parse

def process_beacon(raw_message):
    beacon = parse(raw_message)
    if beacon:
        print(beacon)

client = TelnetClient()
client.connect()

try:
    client.run(callback=process_beacon)
except KeyboardInterrupt:
    print('\nStop ogn gateway')
    client.disconnect()
```

## License
Licensed under the [AGPLv3](LICENSE).
