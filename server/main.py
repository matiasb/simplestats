import logging
import os

from twisted.internet import reactor
from twisted.web import server, static

import settings
from datastore import DataStore
from data_receiver import DataReceiver, SimpleStatsFactory
from data_web import Index


def main():
    logging.basicConfig(filename=os.path.join(settings.ROOT_DIR, 'ss.log'),
                        level=settings.LOG_LEVEL,
                        format='(%(levelname)s) %(asctime)s: %(message)s')

    datastore = DataStore()
    factory = SimpleStatsFactory(datastore)
    web_root = Index(datastore)

    static_path = os.path.join(settings.ROOT_DIR, "web/static")
    web_root.putChild('static', static.File(static_path))
    site = server.Site(web_root)

    reactor.listenTCP(settings.PORT, factory)
    reactor.listenTCP(settings.WEB_PORT, site)

    logging.info("Listening to port %d (TCP client), %d (HTTP)" % (
        settings.PORT, settings.WEB_PORT))

    print "Listening to port %d (TCP client), %d (HTTP)" % (settings.PORT,
                                                            settings.WEB_PORT)
    reactor.run()


if __name__ == '__main__':
    main()
