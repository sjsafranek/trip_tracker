#!/usr/bin/python3
import os
import sys
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

try:
    from tornadouvloop import TornadoUvloop
except ImportError:
    pass


VERSION = {
    'major': 0,
    'minor': 0,
    'patch': 1
}

SERVICE = "TripServer"

import defaults
from router import router

define("port", default=str(defaults.DEFAULT_PORT), help="Server port")

if __name__ == "__main__":
    options.parse_command_line()
    app = router()
    app.listen(options.port)
    print('{0}-{1}.{2}.{3}'.format(SERVICE, VERSION['major'], VERSION['minor'], VERSION['patch']))
    print("Magic happens on http://localhost:"+options.port)
    try:
        IOLoop.configure(TornadoUvloop)
    except NameError:
        pass
    IOLoop.current().start()
