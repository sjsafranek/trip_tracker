#!/usr/bin/python3
from tornado.web import Application
from handlers import *

settings = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"
}

from tinydb import TinyDB, Query
db = TinyDB('db.json')

# router for http server
def router():
    return Application([
        (r"/", MainHandler),
        (r'/api/v1/device', CreateDeviceHandler, dict(database=db)),
        (r'/api/v1/device/(?P<device_id>[^\/]+)', UpdateDeviceHandler, dict(database=db)),
        (r'/api/v1/trip', TripHandler, dict(database=db)),
        # (r'/tms/1.0/(?P<layer>[^\/]+)', ApiTileMap),
        # (r'/tms/1.0/(?P<layer>[^\/]+)/(?P<z>[^\/]+)', ApiTileError),
    ], **settings)
