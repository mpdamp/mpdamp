import logging
import musicpd
import os
import wx

mcEVT_MPD_CONNECTION = wx.NewEventType()
EVT_MPD_CONNECTION = wx.PyEventBinder(mcEVT_MPD_CONNECTION, 1)
class ConnectionEvent(wx.PyCommandEvent):
    """MPD connection event"""
    # pylint: disable=too-few-public-methods
    def __init__(self, value: str):
        """Initialise the event"""
        wx.PyCommandEvent.__init__(self, mcEVT_MPD_CONNECTION, -1)
        self._value = value
    def get_value(self) -> str:
        """Get the value"""
        return self._value

class Connection():
    """Handles executing requests to MPD"""
    # pylint: disable=too-few-public-methods
    def __init__(self, window: wx.Window, config: dict):
        """Initialise the Connection"""
        self.window = window
        self.host = config.get('host', '')
        self.port = config.get('port', '')
        self.username = config.get('username', '')
        self.password = config.get('password', '')

        if not self.host:
            self.host = '127.0.0.1'
        if not self.port:
            self.port = '6600'

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.info("Starting %s", type(self).__name__)

        self.connection_status = None

    def execute(self, func: callable, *args):
        """Execute the provided function with a connected client"""
        #musicpd.CONNECTION_TIMEOUT = 1
        os.environ['MPD_HOST'] = self.host
        os.environ['MPD_PORT'] = self.port
        os.environ['MPD_USERNAME'] = self.username
        os.environ['MPD_PASSWORD'] = self.password
        try:
            self.logger.debug("Connecting to %s:%s", self.host, self.port)
            with musicpd.MPDClient() as client:
                connection_status = "Connected"
                self.logger.debug(connection_status)
                func(client, *args)
        except musicpd.MPDError as e:
            connection_status = "Connection error"
            self.logger.warning("Connection error %s %s", func.__name__, args)
            self.logger.warning(e)
        if self.connection_status != connection_status:
            self.connection_status = connection_status
            wx.PostEvent(self.window, ConnectionEvent(connection_status))
