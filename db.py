#!/usr/bin/env python

import logging
import webapp2
import json
from google.appengine.ext import db
from google.appengine.ext.db import *

class Person(db.Model):
	name = db.StringProperty(required=False, indexed=True)
	number = db.StringProperty(required=False, indexed=True)
	image = db.StringProperty(required=False, indexed=False)
	city = db.StringProperty(required=False, indexed=True)
	state = db.StringProperty(required=False, indexed=True)
	country = db.StringProperty(required=False, indexed=True)

class Party(db.Model):
	phrase = db.StringProperty(required=True, indexed=True)
	count = db.IntegerProperty(required=False, indexed=True)
	source = db.StringProperty(required=False, indexed=True)
	from_person = db.StringProperty(required=False, indexed=True)
	ctime = db.DateTimeProperty(auto_now_add=True, indexed=True)
