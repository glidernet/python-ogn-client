from ogn.client import AprsClient
from ogn.parser import parse, ParseError

def process_beacon(raw_message):
    try:
        beacon = parse(raw_message)
        print('Received {aprs_type}: {raw_message}'.format(**beacon))
    except ParseError as e:
        print('Error, {}'.format(e.message))

client = AprsClient(aprs_user='N0CALL')
client.connect()

try:
    client.run(callback=process_beacon, autoreconnect=True)
except KeyboardInterrupt:
    print('\nStop ogn gateway')
    client.disconnect()