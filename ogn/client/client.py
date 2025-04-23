import socket
import logging
from time import time, sleep

from ogn.client import settings


def create_aprs_login(user_name, pass_code, app_name, app_version, aprs_filter=None):
    if not aprs_filter:
        return f"user {user_name} pass {pass_code} vers {app_name} {app_version}\n"
    else:
        return f"user {user_name} pass {pass_code} vers {app_name} {app_version} filter {aprs_filter}\n"


class AprsClient:
    def __init__(self, aprs_user, aprs_filter='', settings=settings):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

        self.aprs_user = aprs_user
        self.aprs_filter = aprs_filter
        self.settings = settings

        self._sock_peer_ip = None
        self._kill = False

    def connect(self, retries=1, wait_period=15, socket_timeout=5):
        # create socket, connect to server, login and make a file object associated with the socket
        while retries > 0:
            retries -= 1
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                self.sock.settimeout(socket_timeout)

                if self.aprs_filter:
                    port = self.settings.APRS_SERVER_PORT_CLIENT_DEFINED_FILTERS
                else:
                    port = self.settings.APRS_SERVER_PORT_FULL_FEED

                self.sock.connect((self.settings.APRS_SERVER_HOST, port))
                self._sock_peer_ip = self.sock.getpeername()[0]

                login = create_aprs_login(self.aprs_user, -1, self.settings.APRS_APP_NAME, self.settings.APRS_APP_VER, self.aprs_filter)
                self.sock.send(login.encode())
                self.sock_file = self.sock.makefile('rb')

                self._kill = False
                self.logger.info(f"Connect to OGN ({self.settings.APRS_SERVER_HOST}/{self._sock_peer_ip}:{port}) as {self.aprs_user} with filter: '{self.aprs_filter}'" if self.aprs_filter else 'none (full-feed)')
                break
            except (socket.error, ConnectionError) as e:
                self.logger.error(f'Connect error: {e}')
                if retries > 0:
                    self.logger.info(f'Waiting {wait_period}s before next connection try ({retries} attempts left).')
                    sleep(wait_period)
                else:
                    self._kill = True
                    self.logger.critical('Could not connect to OGN.')

    def disconnect(self):
        self.logger.info(f'Disconnect from {self._sock_peer_ip}')
        try:
            # close everything
            self.sock.shutdown(0)
            self.sock.close()
        except OSError:
            self.logger.error('Socket close error')

        self._kill = True

    def run(self, callback, timed_callback=lambda client: None, autoreconnect=False, ignore_decoding_error=True,
            **kwargs):
        while not self._kill:
            try:
                keepalive_time = time()
                while not self._kill:
                    if time() - keepalive_time > self.settings.APRS_KEEPALIVE_TIME:
                        self.logger.info(f'Send keepalive to {self._sock_peer_ip}')
                        self.sock.send('#keepalive\n'.encode())
                        timed_callback(self)
                        keepalive_time = time()

                    # Read packet string from socket
                    packet_b = self.sock_file.readline().strip()
                    packet_str = packet_b.decode(errors="replace") if ignore_decoding_error else packet_b.decode()

                    # A zero length line should not be return if keepalives are being sent
                    # A zero length line will only be returned after ~30m if keepalives are not sent
                    if len(packet_str) == 0:
                        self.logger.warning('Read returns zero length string. Failure.  Orderly closeout from {}'.
                                            format(self._sock_peer_ip))
                        break

                    callback(packet_str, **kwargs)
            except (socket.error, ConnectionError) as e:
                self.logger.error(f'Connect error: {e}')
            except OSError:
                self.logger.error('OSError')
            except UnicodeDecodeError:
                self.logger.error('UnicodeDecodeError')
                self.logger.debug(packet_b)

            if autoreconnect and not self._kill:
                self.connect(retries=100)
            else:
                return


class TelnetClient:
    def __init__(self, settings=settings):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Connect to local telnet server")
        self.settings = settings

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.settings.TELNET_SERVER_HOST, self.settings.TELNET_SERVER_PORT))

    def run(self, callback, autoreconnect=False):
        while True:
            try:
                self.sock_file = self.sock.makefile(mode='rw', encoding='iso-8859-1')
                while True:
                    packet_str = self.sock_file.readline().strip()
                    callback(packet_str)

            except ConnectionRefusedError:
                self.logger.error('Telnet server not running', exc_info=True)

            if autoreconnect:
                sleep(1)
                self.connect()
            else:
                return

    def disconnect(self):
        self.logger.info('Disconnect')
        self.sock.shutdown(0)
        self.sock.close()
