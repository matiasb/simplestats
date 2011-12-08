from twisted.internet import defer
from twisted.trial import unittest
from twisted.web import server
from twisted.web.http import Request
from twisted.web.template import flattenString
from twisted.web.test.test_web import DummyRequest

from server.data_web import Index, ChartDataElement
from server.datastore import DataStore


class IndexResourceTestCase(unittest.TestCase):
    """Test Case for the web root resource."""

    @defer.inlineCallbacks
    def test_render_GET(self):
        """Render SimpleStats main page."""
        datastore = DataStore()
        resource = Index(datastore)

        request = DummyRequest(['foo'])
        d = request.notifyFinish()
        result = resource.render_GET(request)
        self.assertEqual(result, server.NOT_DONE_YET)

        yield d

        element = ChartDataElement(datastore)
        expected = yield flattenString(request, element)

        self.assertIn(expected, ''.join(request.written))

    @defer.inlineCallbacks
    def test_upload_render_POST(self):
        """Upload JSON data file."""
        datastore = DataStore()
        resource = Index(datastore)

        request = DummyRequest(['foo'])
        request.args = {'data_file': ['["var1", 1, 1]\n["var2", 2, 2]'],
                        'upload': 'upload'}

        def fake_redirect(path):
            request.redirect_to = path

        request.redirect = fake_redirect
        d = request.notifyFinish()
        result = resource.render_POST(request)
        self.assertEqual(result, server.NOT_DONE_YET)

        yield d

        self.assertEqual(request.redirect_to, '/')

    @defer.inlineCallbacks
    def test_download_render_POST(self):
        """Download JSON data file."""
        datastore = DataStore()
        datastore.add_value("var1", 1, 1)
        datastore.add_value("var2", 2, 2)
        resource = Index(datastore)

        request = DummyRequest(['foo'])
        request.args = {'download': 'download'}
        d = request.notifyFinish()
        result = resource.render_POST(request)
        self.assertEqual(result, server.NOT_DONE_YET)

        yield d

        expected = '["var1", 1, 1]\n["var2", 2, 2]'
        self.assertEqual(expected, ''.join(request.written))

    @defer.inlineCallbacks
    def test_data_render_POST(self):
        """Main page rendering with data."""
        datastore = DataStore()
        datastore.add_value("var1", 1, 1)
        datastore.add_value("var2", 2, 2)
        resource = Index(datastore)

        request = DummyRequest(['foo'])
        d = request.notifyFinish()
        result = resource.render_GET(request)
        self.assertEqual(result, server.NOT_DONE_YET)

        yield d

        element = ChartDataElement(datastore)
        expected = yield flattenString(request, element)

        self.assertIn(expected, ''.join(request.written))
