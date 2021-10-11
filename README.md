# python-ogn-client

[![Build Status](https://travis-ci.org/glidernet/python-ogn-client.svg?branch=master)](https://travis-ci.org/glidernet/python-ogn-client)
[![PyPi Version](https://img.shields.io/pypi/v/ogn-client.svg)](https://pypi.python.org/pypi/ogn-client)
[![Coverage Status](https://coveralls.io/repos/github/glidernet/python-ogn-client/badge.svg?branch=master)](https://coveralls.io/github/glidernet/python-ogn-client?branch=master)

A python3 module for the [Open Glider Network](http://wiki.glidernet.org/).
It can be used to connect to the OGN-APRS-Servers and to parse APRS-/OGN-Messages.

A full featured gateway with build-in database is provided by [ogn-python](https://github.com/glidernet/ogn-python).


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

### Simple Example:
Connect to OGN and display all incoming beacons.

```python
import asyncio

from ogn.client import AprsClient
from ogn.parser import parse, ParseError


def process_beacon(raw_message):
    try:
        beacon = parse(raw_message)
        print('Received {aprs_type}: {raw_message}'.format(**beacon))
    except ParseError as e:
        print('Error, {}'.format(e.message))
    except NotImplementedError as e:
        print('{}: {}'.format(e, raw_message))


async def run_aprs():
    client = AprsClient(aprs_user='N0CALL')
    await client.connect()
    await client.run(callback=process_beacon, autoreconnect=True)

if __name__ == '__main__':
    try:
        asyncio.run(run_aprs())
    except KeyboardInterrupt:
        print('\nStop ogn gateway')
        # await client.disconnect()

```

### Concurrent Example:
Same as above, but also concurrently execute your custom long-running function:

```python
import asyncio

from ogn.client import AprsClient
from ogn.parser import parse, ParseError


def process_beacon(raw_message):
    try:
        beacon = parse(raw_message)
        print('Received {aprs_type}: {raw_message}'.format(**beacon))
    except ParseError as e:
        print('Error, {}'.format(e.message))
    except NotImplementedError as e:
        print('{}: {}'.format(e, raw_message))


async def run_aprs():
    client = AprsClient(aprs_user='N0CALL')
    await client.connect()
    await client.run(callback=process_beacon, autoreconnect=True)


async def run_another_long_running_function():
    import datetime
    while True:
        print(f'The time is {datetime.datetime.now()}')
        await asyncio.sleep(10)


async def main():
    await asyncio.gather(run_aprs(), run_another_long_running_function())


if __name__ == '__main__':
    asyncio.run(main())
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
