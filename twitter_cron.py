#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from db import *
import logging
import json
import string
import re

class TwitterCronHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		search_term = self.request.get('q')
		if not search_term:
			search_term = 'translationpartytest'
		results = urlfetch.fetch('http://search.twitter.com/search.json?q=%23' + search_term)
		mentions = json.loads(results.content)
		for mention in mentions['results']:
			twitter_id = mention['id_str']
			old_party = Party.all(keys_only=True).filter('external_id', twitter_id).get()
			if old_party is None:
				text = string.replace(mention['text'], '#' + search_term, '')
				text = re.sub(r'\@\w+|\#\w+|https?://\S+', '', text)
				handle = mention['from_user']
				party = Party(phrase=text, source='twitter', from_person=handle)
				party.put()
				person = db.GqlQuery("SELECT * FROM Person WHERE name = :1", handle).get()
				if person is None:
					person = Person(name=handle, image=mention['profile_image_url'])
					person.put()
		template_values['mentions'] = mentions['results']
		return self.response.out.write(template.render('twitter_cron.html', template_values))

app = webapp2.WSGIApplication([
	('/twitter_cron', TwitterCronHandler)
], debug=True)
