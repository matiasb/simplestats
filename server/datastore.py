from collections import defaultdict


class DataStore(defaultdict):
    """Store series data in memory."""

    def __init__(self):
        super(DataStore, self).__init__(list)

    def add_value(self, name, timestamp, value):
        """Add timestamp, value to series 'name'."""
        self[name].append((timestamp, value))

    def series(self):
        """Return series names sorted alphabetically."""
        return sorted(self.iterkeys())
