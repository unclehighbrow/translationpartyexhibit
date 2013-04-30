#!/usr/bin/env python

import webapp2
import json
from google.appengine.ext import db
	
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
			parties = db.GqlQuery("SELECT * FROM Party ORDER BY order DESC LIMIT 10")
			ret['phrases'] = [party_to_dict(party) for party in parties]
		elif op == 'getNewerThanId':
			parties = db.GqlQuery("SELECT * FROM Party WHERE id > :1 ORDER BY id, order DESC LIMIT 10", self.request.get('id'))
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
	ret['partier'] = {'name': "Joe Website"}
	return ret

class Party(db.Model):
	phrase = db.StringProperty(required=True, indexed=True)
	count = db.IntegerProperty(required=False, indexed=True)
	order = db.IntegerProperty(required=False, indexed=True)
	source = db.StringProperty(required=False, indexed=True)
	external_id = db.StringProperty(required=False, indexed=True)
	ctime = db.DateTimeProperty(auto_now_add=True, indexed=True)