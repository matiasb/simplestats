import unittest

from server.datastore import DataStore


class DataStoreTestCase(unittest.TestCase):
    def setUp(self):
        self.datastore = DataStore()

    def test_add_value(self):
        """The values are added under the series name key."""
        self.datastore.add_value('name', 123456789, 42)
        self.assertEqual(len(self.datastore.keys()), 1)
        self.assert_('name' in self.datastore.keys())
        self.assertEqual(len(self.datastore['name']), 1)
        self.assertEqual(self.datastore['name'], [(123456789, 42)])
