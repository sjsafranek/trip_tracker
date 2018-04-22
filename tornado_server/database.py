#!/usr/bin/env python

import lzma
import base64
import builtins
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import defaults
engine = create_engine(
		defaults.DATABASE_FILE,
		convert_unicode=True,
		echo=False
	)

db_session = scoped_session(sessionmaker(autocommit=False,
										 autoflush=False,
										 bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from .Models import *


class Database(object):
	""" Database for OkCupid Model Objects """

	def __init__(self, update=False):
		""" Create database connection """
		self._init_db()
		Session = sessionmaker(bind=engine)
		self.session = Session()
