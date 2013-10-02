#!/usr/bin/env python

import logging
import webapp2
import json
from google.appengine.ext import db
from google.appengine.ext.db import *
from db import *

	
class AjaxHandler(webapp2.RequestHandler):
	def get(self):
		op = self.request.get('op')
		party_id = self.request.get('id')
		ret = {}
		ret['status'] = 'ok'
		if op == 'insert':
			party = Party(phrase=self.request.get('phrase'))
			party.put()
			ret['id'] = party.key().id()
		elif op == 'update':
			party = Party.get_by_id(int(party_id))
			party.count = int(self.request.get('count'))
			party.put()
		elif op == 'getById':
			ret['phrase'] = Party.get_by_id(int(party_id)).phrase
		elif op == 'getRecent':
			parties = db.GqlQuery("SELECT * FROM Party ORDER BY ctime DESC LIMIT 10")
			ret['phrases'] = [party_to_dict(party) for party in parties]
		elif op == 'getNewerThanId':			
			parties = db.GqlQuery("SELECT * FROM Party WHERE __key__ > :1", Key.from_path('Party', int(self.request.get('id'))))
			ret['phrases'] = [party_to_dict(party) for party in parties]
		else:
			ret['status'] = 'error'
		
		#/ajax?op=getRecent
		return self.response.out.write(json.dumps(ret))

app = webapp2.WSGIApplication([
	('/ajax', AjaxHandler)
], debug=True)

def party_to_dict(party):
	ret = {}
	ret['t'] = party.phrase
	ret['id'] = party.key().id()
	ret['count'] = party.count
	partier = None
	if party.source == 'twitter':
		person = db.GqlQuery("SELECT * FROM Person WHERE name = :1", party.from_person).get()
		if person is not None:
			partier = {'name': '@' + person.name, 'image': person.image}
	elif party.source == 'twilio':
		person = db.GqlQuery("SELECT * FROM Person WHERE number = :1", party.from_person).get()
		if person is not None:
			if person.name is not None and person.name != '':
				partier = {'name': person.name}
			else:
				partier = {'name': 'Somebody from ' + person.city}
	if partier is None:
		partier = {'name': 'Somebody'}
	ret['partier'] = partier
	return ret

