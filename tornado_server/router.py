#!/usr/bin/python3
from tornado.web import Application
from handlers import *

settings = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"
}

import defaults
from tinydb import TinyDB, Query
cache = TinyDB(defaults.CACHE_FILE)

import database
db = database.Database()


# router for http server
def router():
    return Application([
        (r"/", MainHandler),
        (r'/api/v1/device', CreateDeviceHandler, dict(cache=cache, database=db)),
        (r'/api/v1/device/(?P<device_id>[^\/]+)/waypoint', InsertDeviceWaypointHandler, dict(cache=cache, database=db)),
        (r'/api/v1/device/(?P<device_id>[^\/]+)/trip', TripHandler, dict(cache=cache, database=db)),
    ], **settings)
