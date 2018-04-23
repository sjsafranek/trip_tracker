#!/usr/bin/python3
import os
from os import getpid
import tornado.gen
import tornado.web
from tornado.web import asynchronous
from tornado.web import RequestHandler
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

import uuid
import time
# import db4iot

from tinydb import Query


class MainHandler(RequestHandler):
    def get(self):
        self.write("TripServer")


class BaseHandler(RequestHandler):

    def initialize(self, cache, database):
        self.Database = database
        self.Trips = cache.table('trips')
        self.Devices = cache.table('devices')

    def sendResponse(self, json_data, status_code=200):
        self.set_status(status_code)
        self.set_header('Content-Type', 'application/json')
        self.write(json_data)

    def missingParamError(self):
         self.sendResponse({
            "status": "error",
            "message":"missing parameter"
        }, 400)

    def invalidDeviceError(self):
         self.sendResponse({
            "status": "error",
            "message":"invalid device"
        }, 400)

    def tripNotFoundError(self):
         self.sendResponse({
            "status": "error",
            "message":"trip not found"
        }, 400)

    def parsePosition(self, position):
        position = position.split(',')
        return [float(position[0]), float(position[1])]

    def deviceIsValid(self, device_id):
        return 0 != len(self.Devices.search(Query().device_id == device_id))




class CreateDeviceHandler(BaseHandler):
    def get(self):
        self.sendResponse({'status': 'ok'})

    def post(self):
        device = {
            "device_id": str(uuid.uuid4())
        }
        self.Devices.insert(device)
        self.sendResponse({"status":"ok", "data": {"device": device}})

    # def delete(self):
    #     self.sendResponse({'status': 'ok'})


class InsertDeviceWaypointHandler(BaseHandler):
    # def get(self):
    #     self.sendResponse({'status': 'ok'})

    def put(self, device_id):
        position = self.get_argument('position')
        print(position)

        if not position or not device_id:
            return self.missingParamError()
        elif not self.deviceIsValid(device_id):
            return self.invalidDeviceError()

        _trips = self.Trips.search(Query().device_id == device_id)
        if 0 == len(_trips):
            return self.tripNotFoundError()
        elif 1 != len(_trips):
            raise ValueError('Database corruption error: More than trip found for id')

        location = self.parsePosition(position)

        device = {}
        device["waypoint__lon"] = location[0]
        device["waypoint__lat"]  = location[1]
        device["device_id"] = device_id
        device["trip_id"] = _trips[0]["trip_id"]
        device["event_timestamp"] = int(time.time())
        self.Devices.update(device, Query().device_id == 'device_id')

        self.Database.insertDeviceWaypoint(device)

        self.sendResponse({"status":"ok", "data": {"device": device}})

    # def post(self):
        # self.sendResponse({'status': 'ok'})

    # def delete(self):
    #     self.sendResponse({'status': 'ok'})


class TripHandler(BaseHandler):
    # def get(self):
    #     self.sendResponse({'status': 'ok'})

    def post(self, device_id):
        trip_id = str(uuid.uuid4())
        event_timestamp = int(time.time())
        position = self.get_argument('position')

        if not self.deviceIsValid(device_id):
            return self.invalidDeviceError()

        if device_id and position:
            location = self.parsePosition(position)
            trip = {
                'device_id': device_id,
                'event_timestamp': event_timestamp,
                'trip_id': trip_id,
                'trip_start_time': event_timestamp,
                'trip_end_time': None,
                'origin__lon': location[0],
                'origin__lat': location[1],
                'destination__lon': None,
                'destination__lat': None
            }

            self.Trips.remove(Query().device_id == device_id)
            self.Trips.insert(trip)
            return self.sendResponse({"status":"ok", "data": {"trip": trip}})

        self.missingParamError()

    def delete(self, device_id):
        position = self.get_argument('position')

        if not self.deviceIsValid(device_id):
            return self.invalidDeviceError()

        if device_id and position:
            location = self.parsePosition(position)
            trips = self.Trips.search(Query().device_id == device_id)
            for trip in trips:
                self.Trips.remove(Query().device_id == device_id)
                trip['trip_end_time'] = int(time.time())
                trip['destination__lon'] = location[0]
                trip['destination__lat'] = location[1]

                self.Database.insertDeviceTrip(trip)

                return self.sendResponse({"status":"ok", "data": {"trip": trip}})

        return self.missingParamError()



'''

class ApiTile(BaseHandler):
    # https://gist.github.com/methane/2185380
    executor = ThreadPoolExecutor(max_workers=config.MAX_WORKERS)

    # def sendTile(self, tile):
        # cache_map_tile(tile, layer, z, x, y)
        # Return image
        # self.sendPngResponse(tile)

    @run_on_executor
    def background_task(self, layer_id, z, x, y):
        folder = os.path.join(config.LAYER_DIR,layer_id)
        if not os.path.exists(folder):
            raise ValueError("files not found")

        if not Maps.hasMap(layer_id):
            # Create map
            m = mapnik.Map(tile.TILE_WIDTH, tile.TILE_HEIGHT)
            # Load mapnik xml stylesheet
            stylesheet = os.path.join(config.LAYER_DIR, str(layer_id), config.STYLESHEET)
            mapnik.load_map(m, stylesheet)
            # Zoom to all features
            m.zoom_all()
            # Render Map Tile
            Maps.addMap(layer_id, m)

        job_id = self.getRequestId()

        renderer = Maps.getMap(layer_id)
        # im = renderer.renderTile(z, x, y, job_id, responseHandler=self)
        im = renderer.renderTile(z, x, y, job_id)
        return im

    @asynchronous
    @tornado.gen.coroutine
    def get(self, layer, z, x, y):
        # TODO:
        #  - Move to __init__()
        self.generateRequestId()
        self.layer_id = layer

        z = int(z)
        x = int(x)
        y = y.replace('.png', '')
        y = int(y)

        im = get_cached_map_tile(layer, z, x, y)
        if im:
            self.sendPngResponse(im)
            return


        im = yield self.background_task(layer, z, x, y)

        # save map tile
        cache_map_tile(im, layer, z, x, y)

        # Return image
        self.sendPngResponse(im)

    # Cancel tile rendering
    # https://stackoverflow.com/questions/25327455/right-way-to-timeout-a-request-in-tornado
    def on_connection_close(self):
        # TODO: cancel tile rendering
        print('closed', self)
        Maps.getMap(self.layer_id).cancelTile(
                                self.getRequestId())
        # self.finish()

'''
