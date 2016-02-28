# ogn-python

[![Build Status](https://travis-ci.org/glidernet/ogn-python.svg?branch=master)]
(https://travis-ci.org/glidernet/ogn-python)
[![Coverage Status](https://img.shields.io/coveralls/glidernet/ogn-python.svg)]
(https://coveralls.io/r/glidernet/ogn-python)
[![PyPi Version](https://img.shields.io/pypi/v/ogn-python.svg)]
(https://pypi.python.org/pypi/ogn-python)

A python module for the [Open Glider Network](http://wiki.glidernet.org/).
The submodule 'ogn.gateway' is an aprs client which could be invoked via a CLI
or used by other python projects.
The CLI allows to save all received beacons into a database with [SQLAlchemy](http://www.sqlalchemy.org/).
The [sqlite](https://www.sqlite.org/)-backend is sufficient for simple testing,
but some tasks (e.g. logbook generation) require a proper backend like [postgresql](http://www.postgresql.org/).
An external python project would instantiate ogn.gateway and register a custom callback,
called each time a beacon is received.

[Examples](https://github.com/glidernet/ogn-python/wiki/Examples)


## Usage
Implement your own gateway by using ogn.gateway with a custom callback function.
Each time a beacon is received, this function gets called and
lets you process the incoming data.

Example:
```python
#!/usr/bin/env python3
from ogn.gateway.client import ognGateway
from ogn.parser.parse import parse_aprs, parse_ogn_beacon
from ogn.parser.exceptions import ParseError


def process_beacon(raw_message):
    if raw_message[0] == '#':
        print('Server Status: {}'.format(raw_message))
        return

    try:
        message = parse_aprs(raw_message)
        message.update(parse_ogn_beacon(message['comment']))

        print('Received {beacon_type} from {name}'.format(**message))
    except ParseError as e:
        print('Error, {}'.format(e.message))


if __name__ == '__main__':
    gateway = ognGateway(aprs_user='N0CALL')
    gateway.connect()

    try:
        gateway.run(callback=process_beacon, autoreconnect=True)
    except KeyboardInterrupt:
        print('\nStop ogn gateway')

    gateway.disconnect()
```


## License
Licensed under the [AGPLv3](LICENSE).
