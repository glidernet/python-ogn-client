from ogn.client.client import AprsClient    # noqa: F401
from ogn.client.client import TelnetClient  # noqa: F401


class CustomSettings(object):
    def __init__(self, **kw):
        self.kw = kw

    def __getattr__(self, name):
        return self.kw[name]
