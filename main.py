#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp import template

class MainHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		return self.response.out.write(template.render('index.html', template_values))

app = webapp2.WSGIApplication([
	('/', MainHandler)
], debug=True)
