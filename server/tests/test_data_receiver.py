import logging

from twisted.trial import unittest
from twisted.test import proto_helpers

from server import settings
from server.data_receiver import HINT, DataReceiver, SimpleStatsFactory
from server.datastore import DataStore

logging.disable(logging.CRITICAL)


class DataReceiverTestCase(unittest.TestCase):
    def setUp(self):
        datastore = DataStore()
        self.factory = SimpleStatsFactory(datastore)
        self.proto = self.factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)
        # clear welcome message
        self.tr.clear()

    def test_send_invalid_data(self):
        self.proto.dataReceived('invalid data\r\n')
        self.assertEqual(self.tr.value(), HINT + '\r\n')

    def test_send_invalid_json_data(self):
        self.proto.dataReceived("['asd', ]\r\n")
        self.assertEqual(self.tr.value(), HINT + '\r\n')

    def test_valid_data_is_added(self):
        self.proto.dataReceived('["var1", 3232153021, 10.5]\r\n')
        self.assertEqual(self.tr.value(), '--OK\r\n')
        self.assertTrue('var1' in self.factory.data.keys())
        self.assertEqual(len(self.factory.data['var1']), 1)
        self.assertEqual(self.factory.data['var1'][0], (3232153021, 10.5))
