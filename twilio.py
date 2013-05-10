#!/usr/bin/env python

import logging
import webapp2
from google.appengine.ext.webapp import template
from db import *

class TwilioHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		message_id = self.request.get('SmsSid')
		from_number = self.request.get('From')
		from_city = self.request.get('FromCity')
		from_state = self.request.get('FromState')
		from_zip = self.request.get('FromZip')
		from_country = self.request.get('FromCountry')
		body = self.request.get('Body')
		
		person = db.GqlQuery("SELECT * FROM Person WHERE number = :1", from_number).get()
		if person is None: # first text
			party = Party(phrase=body, source='twilio', from_person=from_number)
			party.put()
			person = Person(number=from_number, city=from_city, state=from_state, country=from_country)
			person.put()
			template_values['holler_back'] = "Thanks! What's your name?"
		elif person.name is None or person.name == '': # second text, telling us their name
			person.name = body
			person.put()
			template_values['holler_back'] = "Great! You'll be up on the board soon!"
		else: # they're still texting
			template_values['holler_back'] = "You've got more? Keep em coming!"
			party = Party(phrase=body, source='twilio', from_number=from_number)
			party.put()
			
		return self.response.out.write(template.render('twilio.xml', template_values))

app = webapp2.WSGIApplication([
	('/twilio', TwilioHandler)
], debug=True)