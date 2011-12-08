import json
import logging
import operator
import os

from twisted.web import resource, server
from twisted.web.template import Element, flatten, renderer, XMLFile
from twisted.web.util import redirectTo

import settings


class Index(resource.Resource):
    """Web root resource."""
    isLeaf = False

    def __init__(self, datastore):
        resource.Resource.__init__(self)
        self.datastore = datastore

    def _load_serialized_data(self, data):
        """Load data from \n-separated JSON tuples: ["name", ts, value]."""
        json_decoded = []
        json_tuples = data.splitlines()
        for json_tuple in json_tuples:
            try:
                series_data = json.loads(json_tuple)
                self.datastore.add_value(*series_data)
            except TypeError, e:
                logging.exception(e)
                continue
            except ValueError, e:
                logging.exception(e)
                continue

    def _serialize_data(self):
        """Return \n-separated JSON tuples with current data."""
        data = []
        for series in self.datastore.series():
            for ts, value in self.datastore[series]:
                json_tuple = json.dumps((series, ts, value))
                data.append(json_tuple)
        return '\n'.join(data)

    def getChild(self, name, request):
        """Check if request is for index or a children."""
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        """Render SimpleStats main page."""
        request.write("<!DOCTYPE html>\n")
        data_element = ChartDataElement(self.datastore)
        d = flatten(request, data_element, request.write)

        def done(_):
            request.finish()
            return _

        d.addBoth(done)
        return server.NOT_DONE_YET

    def render_POST(self, request):
        """Process form POST for data download/upload."""
        if 'upload' and 'data_file' in request.args:
            data = request.args['data_file'][0]
            self._load_serialized_data(data)
            request.redirect('/')
            request.finish()
        elif 'download' in request.args:
            request.setHeader('Content-Type', 'application/json')
            request.setHeader('Content-Disposition',
                              'attachment; filename=simplestats.json')
            serialized_data = self._serialize_data()
            request.write(serialized_data)
            request.finish()
        else:
            return self.render_GET(request)
        # this is the way to do it, according to documentation
        return server.NOT_DONE_YET


class ChartDataElement(Element):
    """Element renderer for series plots."""
    loader = XMLFile(os.path.join(settings.ROOT_DIR,
                                  'web/templates/index.html'))

    def __init__(self, datastore):
        Element.__init__(self)
        self.datastore = datastore

    @renderer
    def series_row(self, request, tag):
        """Render each series stats row."""
        data = self.datastore
        for series in data.series():
            series_data = [v for ts, v in data[series]]
            yield tag.clone().fillSlots(
                    name=series,
                    count=str(len(series_data)),
                    max=str(max(series_data)),
                    min=str(min(series_data)),
                    avg=str(sum(series_data) / len(series_data)))

    @renderer
    def json_data(self, request, tag):
        """Render the data as a javascript JSON array."""
        data = {}
        for series in self.datastore.series():
            milisecs_data = map(lambda (ts, v): (ts * 1000, v),
                                self.datastore[series])
            series_data = {
                'label': series,
                'data': sorted(milisecs_data, key=operator.itemgetter(0))}
            data[series] = series_data
        json_encoded = json.dumps(data)
        return tag('var data = %s;' % json_encoded)
