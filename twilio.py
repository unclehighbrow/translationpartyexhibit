#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp import template
from ajax import * 

class TwilioHandler(webapp2.RequestHandler):
	def get(self):
		party = Party(phrase=self.request.get('Body'), source='twilio', order=0)
		party.put()
		template_values = {}
		return self.response.out.write(template.render('twilio.xml', template_values))

app = webapp2.WSGIApplication([
	('/twilio', TwilioHandler)
], debug=True)
