import json
import logging
import time

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


HINT = '--Hint: send data of the form [name:str, timestamp:float, data:float]'


class DataReceiver(LineReceiver):
    """Receiver for JSON tuples data."""

    def connectionMade(self):
        """Send client a welcome message."""
        self.sendLine(HINT)

    def lineReceived(self, line):
        """Process a line received from the client."""
        # load json
        logging.debug('Received data: %s', line)
        try:
            data = json.loads(line)
        except ValueError, e:
            # invalid json
            logging.exception(e)
            self.sendLine(HINT)
            return

        try:
            data[1] = float(data[1])
            data[2] = float(data[2])
        except (TypeError, ValueError), e:
            logging.exception(e)
            self.sendLine(HINT)
            return

        # validate/clean data
        if not isinstance(data, list) or len(data) != 3 or \
           not isinstance(data[0], basestring):
            logging.debug("Invalid data: %s", repr(data))
            self.sendLine(HINT)
            return

        # append
        self.factory.data.add_value(*data)
        self.sendLine('--OK')


class SimpleStatsFactory(Factory):
    """SimpleStats server factory."""
    protocol = DataReceiver

    def __init__(self, datastore):
        self.data = datastore
