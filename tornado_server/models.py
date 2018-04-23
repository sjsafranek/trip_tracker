#!/usr/bin/python

from database import Base

import datetime
from sqlalchemy import ForeignKey
# from sqlalchemy.sql import func
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref


class Trip(Base):
    """ trips table """
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_start_time = Column(Integer)
    trip_end_time = Column(Integer)
    device_id = Column(String(50))
    trip_id = Column(String(50))
    origin__lon = Column(Float)
    origin__lat = Column(Float)
    destination__lon = Column(Float)
    destination__lat = Column(Float)

    def __init__(self, data):
        self.trip_start_time = data['trip_start_time']
        self.trip_end_time = data['trip_end_time']
        self.device_id = data['device_id']
        self.trip_id = data['trip_id']
        self.origin__lon = data['origin__lon']
        self.origin__lat = data['origin__lat']
        self.destination__lon = data['destination__lon']
        self.destination__lat = data['destination__lat']

    def __repr__(self):
        return '<Trip %r>' % (self.trip_id)


class Waypoint(Base):
    """ waypoints table """
    __tablename__ = 'waypoints'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_timestamp = Column(Integer)
    device_id = Column(String(50))
    trip_id = Column(String(50))
    waypoint__lon = Column(Float)
    waypoint__lat = Column(Float)

    def __init__(self, data):
        self.event_timestamp = data['event_timestamp']
        self.device_id = data['device_id']
        self.trip_id = data['trip_id']
        self.waypoint__lon = data['waypoint__lon']
        self.waypoint__lat = data['waypoint__lat']

    def __repr__(self):
        return '<Waypoint %r>' % (self.trip_id)
