#!/usr/bin/env python
# coding=utf=8
import datetime
import json
import logging
import re
import random
import time
from urllib2 import quote
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from db import *

class TwilioHandler(webapp2.RequestHandler):
	def get(self):
		BE_TRANSLATE = True
		

		template_values = {}
		message_id = self.request.get('SmsSid')
		from_number = self.request.get('From')
		from_city = self.request.get('FromCity')
		from_state = self.request.get('FromState')
		from_zip = self.request.get('FromZip')
		from_country = self.request.get('FromCountry')
		body = self.request.get('Body')

		try:
			if re.match(r'.*?(fuck|shit|\b(anal|anus|arse|ass|ball\s*sack?|balls|bastard|bitch|biatch|bloody|blowjob|blow job|bollock|bollok|boner|boob|bugger|butt|buttplug|clitoris|cock|coon|crap|cunt|damn|dick|dildo|dyke|fag|feck|fellate|fellatio|felching|fuck|f u c k|fudgepacker|fudge packer|gay|Goddamn|God damn|hell|homo|jizz|knobend|knob end|labia|muff|nigger|nigga|penis|piss|poop|prick|pube|pussy|queer|scrotum|shit|s hit|sh1t|slut|smegma|spunk|tit|tosser|turd|twat|vagina|wank|whore)(e?s)?\b).*', body, re.IGNORECASE):
				template_values['holler_back'] = "Hey, now. This is a family museum. Let's keep it clean."
				return self.response.out.write(template.render('twilio.xml', template_values))

			if BE_TRANSLATE:
				finished = False
				lang = 'en'
				phrase_queue = []
				last_result = body
				phrase_queue.append({'lang': lang, 'string': last_result})
				while not finished:
					translated_text = translate(last_result, lang)
					if lang == 'en':
						lang = 'ja'
					else:
						lang = 'en'
					phrase_queue.append({'lang': lang, 'string': translated_text})
					if len(phrase_queue) > 3 and phrase_queue[len(phrase_queue) - 1]['lang'] == 'en' and phrase_queue[len(phrase_queue) - 1]['string'] == phrase_queue[len(phrase_queue) - 3]['string']:
							finished = True
							break
					elif len(phrase_queue) >= 21:
						finished = True
						break
					else:
						#logging.error(translated_text)
						last_result = translated_text
				if len(phrase_queue) <= 5:

					if len(body.split(' ')) < 5:
						template_values['holler_back'] = "That one's a little short. I think you can do better. Try a famous quote or a song lyric!"
					else:
						template_values['holler_back'] = "I don't think that one's going to be that good. I think you can do better. Try a famous quote or a song lyric!"

					return self.response.out.write(template.render('twilio.xml', template_values))

			# this happens if be translate is on or not
			person = db.GqlQuery("SELECT * FROM Person WHERE number = :1", from_number).get()
			if person is None: # first text
				party = Party(phrase=body, source='twilio', from_person=from_number, ctime=datetime.datetime.now().replace(microsecond=0))
				person = Person(number=from_number, city=from_city, state=from_state, country=from_country)
				person.put()
				template_values['holler_back'] = "Thanks!  You'll be up on the board soon!"
			#elif person.name is None or person.name == '': # second text, telling us their name
			#	person.name = body
			#	person.put()
			#	template_values['holler_back'] = "Great!"
			else: # they're still texting
				template_values['holler_back'] = "You've got more? Keep em coming!"
				party = Party(phrase=body, source='twilio', from_person=from_number, ctime=datetime.datetime.now().replace(microsecond=0))

			if (BE_TRANSLATE):
				party.json = json.dumps(phrase_queue, ensure_ascii=False)
			party.rando = random.randint(1, 1000)
			party.put()
		except Exception as e:
			template_values['holler_back'] = 'Wow, this is embarassing. Something super technical and confusing went wrong, can you try again in a little while?'
			logging.error('bad: ' + str(e))

		return self.response.out.write(template.render('twilio.xml', template_values))


def translate(phrase, in_lang):
	if in_lang == 'en':
		out_lang = 'ja'
	else:
		out_lang = 'en'
	
	if True:
		url = 'http://api.microsofttranslator.com/V2/Ajax.svc/GetTranslations?appId=F2926FC35C3732CEC3E9C92913745F9C28912821&from=' + in_lang + '&to=' + out_lang + '&maxTranslations=1'
		url += '&text=' + quote(phrase.encode('utf-8'))

		response = urlfetch.fetch(url=url)
	
		content = re.sub(u'\xEF\xBB\xBF', '', response.content)
		data = json.loads(content)
		translated_text = data['Translations'][0]['TranslatedText']
		time.sleep(.1)
	else:
		url = 'https://www.googleapis.com/language/translate/v2?'
		url += '&source=' + in_lang
		url += '&target=' + out_lang
		url += '&q=' + quote(phrase.encode('utf-8'))
		url += '&key=' + 'AIzaSyAI3PoUAJ_uP0o33EDgUfSEUMALepQAaNA'
		
		content = urlfetch.fetch(url=url).content
		data = json.loads(content)
		
		translated_text = data['data']['translations'][0]['translatedText']
		
		
		
	return translated_text


app = webapp2.WSGIApplication([
	('/twilio', TwilioHandler)
], debug=True)