#!/usr/bin/env python

import logging
import webapp2
import json
import random
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
		elif op == 'getNewerThanTime':
			parties = db.GqlQuery("SELECT * FROM Party WHERE ctime > DATETIME(:1)", self.request.get('ctime'))
			res = [party_to_dict(party) for party in parties]
			exclude_ids = []
			if self.request.get('exclude_ids'):
				exclude_ids = self.request.get('exclude_ids').split(',')
			if exclude_ids:
				final_res = []
				for party in res:
					if not party['id'] in exclude_ids:
						final_res.append(party)
				res = final_res			
			ret['phrases'] = res
		elif op == 'getNewerThanCursor':
			parties = Party.all()
			cursor = self.request.get('cursor')
			if cursor:
				parties.with_cursor(start_cursor=cursor)
			ret['phrases'] = [party_to_dict(party) for party in parties]
			ret['cursor'] = str(parties.cursor())
		elif op == 'getRandom':
			rando = random.randint(1, 1000)
			parties = db.GqlQuery("SELECT * FROM Party WHERE rando > :1 ORDER BY rando LIMIT 1", rando)
			res = [party_to_dict(party) for party in parties]
			if not res:
				parties = db.GqlQuery("SELECT * FROM Party WHERE rando < :1 ORDER BY rando DESC LIMIT 1", rando)
				res = [party_to_dict(party) for party in parties]
			ret['phrases'] = res
		else:
			ret['status'] = 'error'
		
		#/ajax?op=getRecent
		return self.response.out.write(json.dumps(ret, ensure_ascii=False))

app = webapp2.WSGIApplication([
	('/ajax', AjaxHandler)
], debug=True)

def party_to_dict(party):
	ret = {}
	ret['t'] = party.phrase
	ret['id'] = str(party.key().id())
	ret['count'] = party.count
	ret['ctime'] = str(party.ctime + datetime.timedelta(seconds=1))[0:19]
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
	if (party.json):
		ret['phrase_queue'] = json.loads(party.json)
	return ret

