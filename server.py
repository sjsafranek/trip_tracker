# from tornado.wsgi import WSGIContainer
# from tornado.httpserver import HTTPServer
# from tornado.ioloop import IOLoop
from flask import request
from flask import jsonify
from flask import Flask
from flask_cors import CORS

import uuid
import time
import db4iot

app = Flask(__name__)
CORS(app)

from tinydb import TinyDB, Query
db = TinyDB('db.json')
Trips = db.table('trips')
Devices = db.table('devices')
# print(table.all())


def parsePosition(position):
    position = position.split(',')
    return [float(position[0]), float(position[1])]


def deviceIsValid(device_id):
    return 0 != len(Devices.search(Query().device_id == device_id))


@app.route("/api/v1/device", methods=["POST"])
def createDevice():
    device = {
        "device_id": str(uuid.uuid4())
    }
    Devices.insert(device)
    return jsonify({"status":"ok", "data": {"device": device}})


@app.route("/api/v1/device/<device_id>", methods=["PUT"])
def updateDevice(device_id):
    position = request.args.get('position')
    if not position or not device_id:
        print({"status":"error", "message":"missing parameter"})
        return jsonify({"status":"error", "message":"missing parameter"})
    elif not deviceIsValid(device_id):
        print({"status":"error", "message":"invalid device"})
        return jsonify({"status":"error", "message":"invalid device"})

    _trips = Trips.search(Query().device_id == device_id)
    if 0 == len(_trips):
        print(({"status":"error", "message":"no trip found"}))
        return jsonify({"status":"error", "message":"no trip found"})
    elif 1 != len(_trips):
        print({"status":"error", "message":"more than one trip found"})
        return jsonify({"status":"error", "message":"more than one trip found"})

    location = parsePosition(position)

    device = {}
    device["waypoint__lon"] = location[0]
    device["waypoint__lat"]  = location[1]
    device["device_id"] = device_id
    device["event_timestmap"] = int(time.time())
    Devices.update(device, Query().device_id == 'device_id')

    print({"status":"ok", "data": {"device": device}})
    return jsonify({"status":"ok", "data": {"device": device}})


@app.route("/api/v1/location", methods=["POST"])
def location():
    device_id = request.args.get('device_id')
    return updateDevice(device_id)


@app.route("/api/v1/trip/end", methods=["POST"])
@app.route("/api/v1/trip", methods=["POST"])
def createTrip():
    trip_id = str(uuid.uuid4())
    event_timestmap = int(time.time())
    device_id = request.args.get('device_id')
    position = request.args.get('position')

    if not deviceIsValid(device_id):
        return jsonify({"status":"error", "message":"invalid device"})

    if device_id and position:
        location = parsePosition(position)
        trip = {
            'device_id': device_id,
            'event_timestmap': event_timestmap,
            'trip_id': trip_id,
            'trip_start_time': event_timestmap,
            'trip_end_time': None,
            'origin__lon': location[0],
            'origin__lat': location[1],
            'destination__lon': None,
            'destination__lat': None
        }

        Trips.remove(Query().device_id == device_id)
        Trips.insert(trip)
        print({"status":"ok", "data": {"trip": trip}})
        return jsonify({"status":"ok", "data": {"trip": trip}})

    print({"status":"error", "message":"missing parameter"})
    return jsonify({"status":"error", "message":"missing parameter"})


@app.route("/api/v1/trip", methods=["DELETE"])
def deleteTrip():
    position = request.args.get('position')
    device_id = request.args.get('device_id')

    if not deviceIsValid(device_id):
        return jsonify({"status":"error", "message":"invalid device"})

    if device_id and position:
        location = parsePosition(position)
        trips = Trips.search(Query().device_id == device_id)
        for trip in trips:
            Trips.remove(Query().device_id == device_id)
            trip['trip_end_time'] = int(time.time())
            trip['destination__lon'] = location[0]
            trip['destination__lat'] = location[1]
            return jsonify({"status":"ok", "data": {"trip": trip}})
            print({"status":"ok", "data": {"trip": trip}})

    print({"status":"error", "message":"missing parameter"})
    return jsonify({"status":"error", "message":"missing parameter"})


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True
    )





# http_server = HTTPServer(WSGIContainer(app))
# http_server.listen(5000)
# IOLoop.instance().start()


# # Tornado settings
# settings = {
# 	'static_path': os.path.join(os.getcwd(), 'static'),
# 	# 'template_path': os.path.join(os.getcwd(), 'templates'),
# 	'debug': True
# }
#
# if __name__ == "__main__":
# 	parse_command_line()
# 	application = tornado.web.Application([
# 		(r"/", MainHandler),
# 		(r"/db", DatabaseHandler),
# 		(r"/words", WordsHandler),
# 		(r"/map/([a-zA-Z]+)", MapHandler),
# 		(r"/set/([a-zA-Z]+)/([a-zA-Z]+)", SetHandler),
# 		(r"/dictionary/([a-zA-Z]+)",DictionaryHandler),
# 		(r"/thesaurus/([a-zA-Z]+)", ThesaurusHandler),
# 	], **settings)
# 	application.listen(options.p)
# 	logger.info("Running on http://localhost:" + str(options.p))
# 	tornado.ioloop.IOLoop.current().start()
