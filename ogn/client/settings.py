import importlib.metadata

APRS_SERVER_HOST = 'aprs.glidernet.org'
APRS_SERVER_PORT_FULL_FEED = 10152
APRS_SERVER_PORT_CLIENT_DEFINED_FILTERS = 14580

APRS_APP_NAME = 'python-ogn-client'

try:
    PACKAGE_VERSION = importlib.metadata.version('ogn-client')
except importlib.metadata.PackageNotFoundError:
    PACKAGE_VERSION = '0.0.0'

APRS_APP_VER = PACKAGE_VERSION[:3]

APRS_KEEPALIVE_TIME = 240

TELNET_SERVER_HOST = 'localhost'
TELNET_SERVER_PORT = 50001
