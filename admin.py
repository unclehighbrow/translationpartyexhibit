#!/usr/bin/env python

import logging
import webapp2
import json
import random
from google.appengine.ext import db
from google.appengine.ext.db import *
from db import *
from ajax import party_to_dict
from google.appengine.ext.webapp import template
import webapp2
from datetime import date, timedelta

	
class AdminHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		if self.request.get('delete_party'):
			logging.error('dick')
		elif self.request.get('delete_curse'):
			logging.error('dick')
		elif self.request.get('new_curse'):
			logging.error('dick')
		else:
			parties = db.GqlQuery("SELECT * FROM Party WHERE ctime > :1", date.today() - timedelta(1))
			template_values['parties'] = [party_to_dict(party) for party in parties]

		return self.response.out.write(template.render('admin.html', template_values))
		
		
app = webapp2.WSGIApplication([
	('/admin', AdminHandler)
], debug=True)