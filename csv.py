#!/usr/bin/env python

import logging
import webapp2
import json
import random
from google.appengine.ext import db
from google.appengine.ext.db import *
from db import *

	
class CsvHandler(webapp2.RequestHandler):
	def get(self):
		parties = db.GqlQuery("SELECT * FROM Party ORDER BY ctime DESC LIMIT 10")
		for party in parties:
			self.response.out.write(party.phrase)
		
app = webapp2.WSGIApplication([
	('/csv', CsvHandler)
], debug=True)