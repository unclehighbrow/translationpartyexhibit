#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
import json

class TwitterCronHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		search_term = self.request.get('q')
		if not search_term:
			search_term = '#mminyc'
		results = urlfetch.fetch('http://search.twitter.com/search.json?q=' + search_term)
		mentions = json.loads(results.content)
		template_values['mentions'] = mentions['results']
		return self.response.out.write(template.render('twitter_cron.html', template_values))

app = webapp2.WSGIApplication([
	('/twitter_cron', TwitterCronHandler)
], debug=True)
