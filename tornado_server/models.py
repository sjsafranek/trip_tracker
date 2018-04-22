#!/usr/bin/python

from .Database import Base

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


class Trips(Base):
    """ trips table """
    __tablename__ = 'trips'
    trip_start_time = Column(Integer)
    trip_end_time = Column(Integer)
    device_id = Column(String(50))
    trip_id = Column(String(50))
    origin__lon = Column(Float)
    origin__lat = Column(Float)
    destination__lon = Column(Float)
    destination__lat = Column(Float)

    # def __init__(self, username):
        # self.username = username

    def __repr__(self):
        return '<Trip %r>' % (self.trip_id)


class Waypoints(Base):
    """ waypoints table """
    __tablename__ = 'waypoints'
    event_timestamp = Column(Integer)
    device_id = Column(String(50))
    trip_id = Column(String(50))
    waypoint__lon = Column(Float)
    waypoint__lat = Column(Float)

    # def __init__(self, username):
        # self.username = username

    def __repr__(self):
        return '<Waypoint %r>' % (self.trip_id)
