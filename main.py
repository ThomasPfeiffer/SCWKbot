# -*- coding: utf-8 -*-

import StringIO
import json
import logging
import random
import urllib
import urllib2
import Logic.Responder as Responder
import Entity.User
import Entity.Event
import Logic.UserController as UserController
import Test.EventTest
import datetime

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

from extoken import TOKEN

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class Setting(ndb.Model):
	value = ndb.StringProperty()

class CurrentUpdate(ndb.Model):
	# key name: str(chat_id)
	updateID = ndb.IntegerProperty()


# ================================

def setCurrentUpdate(chatID, updateID):
	logging.info('Setting current update for ' + str(chatID) + " to " + str(updateID))
	update = CurrentUpdate.get_or_insert(str(chatID))
	update.updateID = updateID
	update.put()

def getCurrentUpdate(chatID):
	update = CurrentUpdate.get_by_id(str(chatID))
	if update:
		return update.updateID
	return -1

def setSetting(setting, value):
	setting = Setting.get_or_insert(setting)
	setting.value = value
	setting.put()

def getSetting(setting):
	s = Setting.get_by_id(setting)
	if s:
		return s.value

# ================================

def send(msg, chat_id):
			if msg:
				replyKeyboardMakeup = {"keyboard": [['Anmelden'], ['Abmelden']], "one_time_keyboard": True} 
				resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
					'chat_id': str(chat_id),
					'text': msg.encode("utf-8"),
					'disable_web_page_preview': 'true',
					'reply_markup': json.dumps(replyKeyboardMakeup)
				})).read()
			else:
				logging.error('no msg specified')
				resp = None

			logging.info('send response:')
			logging.info(resp)

class ReminderHandler(webapp2.RequestHandler):
	def get(self):
		event = Entity.Event.getNextEvent()
		if event and not event.reminderSent:
			if event.date <= datetime.datetime.now() + datetime.timedelta(hours=12):
				allUsers = Entity.User.getAll()
				for user in allUsers:
					if user.key not in event.registeredUsers and user.key not in event.cancelledUsers:
						send(u'Du hast dich noch nicht für ein bald stattfindendes Event an- oder abgemeldet: \n' + event.toString() + u'\n\n Bitte antworte mit an oder ab um dich an- oder abzumelden.' , user.chatID)
				event.reminderSent = True
				event.put()

class MeHandler(webapp2.RequestHandler):
	def get(self):
		urlfetch.set_default_fetch_deadline(60)
		self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
	def get(self):
		urlfetch.set_default_fetch_deadline(60)
		self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
	def get(self):
		urlfetch.set_default_fetch_deadline(60)
		url = self.request.get('url')
		if url:
			self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
	def post(self):
		urlfetch.set_default_fetch_deadline(60)
		body = json.loads(self.request.body)
		logging.info('request body:')
		logging.info(body)
		self.response.write(json.dumps(body))

		update_id = body['update_id']
		message = body['message']
		message_id = message.get('message_id')
		date = message.get('date')
		text = message.get('text')
		fr = message.get('from')
		chat = message['chat']
		chat_id = chat['id']

		if not text:
			logging.info('no text')
			return

		def reply(msg=None):
			if msg:
				resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
					'chat_id': str(chat_id),
					'text': msg.encode("utf-8"),
					'disable_web_page_preview': 'true',
				})).read()
			else:
				logging.error('no msg specified')
				resp = None

			logging.info('send response:')
			logging.info(resp)

		lastUpdate = getCurrentUpdate(chat_id)
		if lastUpdate >= update_id:
			logging.info('Already at update ' + str(lastUpdate))
			return
		else:
			setCurrentUpdate(chat_id, update_id)

		if getSetting('userRegistration') != 'True' and not Entity.User.get(str(fr['id'])):
			reply('Registrierung ist geschlossen.')
			return

		# COMMANDS
		if text.startswith('/'):
			if UserController.isAdmin(str(fr['id'])):
				if text == '/start':
					reply(u'Bot enabled')
					setSetting('enabled', 'True')
					return
				if text == '/stop':
					reply(u'Bot disabled')
					setEnabled('enabled','False')
					return
				if text == '/enableUserRegistration':
					reply(u'User registration enabled')
					setSetting('userRegistration', 'True')
					return
				if text == '/disableUserRegistration':
					reply(u'User registration disabled')
					setSetting('userRegistration', 'False')
					return
				if text == '/listUsers':
					allUsers = Entity.User.getAll()
					answer = u''
					for user in allUsers:
						answer = answer + user.firstName + u'\n'
					reply(answer)
					return
				if text.startswith('/deleteUser '):
					if UserController.deleteUser(str(fr['id']) , text.split()[1]):
						reply(u'User ' + text.split()[1] + u' deleted.')
						return
				if text.startswith('/setAdmin'):
					split = text.split()
					if len(split) == 3:
						if UserController.setAdmin(str(fr['id']), split[1], (split[2] == 'True')):
							reply(u'User ' + split[1] + u' admin set to ' + split[2])
							return
						else:
							logging.warn("Set Admin request by " + str(fr['id']) + " not successful.")




		# END COMMANDS
		if getSetting('enabled') != 'True':
			logging.info('Bot is disabled')
			return

		# For dev
		if '/setName' in text:
			split = text.split()
			senderFirstName = split[split.index('/setName')+1]
			del split[split.index('/setName')+1]
			split.remove('/setName')
			text = ' '.join(split)
			message['text']=text
			message['from']['first_name']=senderFirstName


		if '/setUser' in text:
			split = text.split()
			senderID = split[split.index('/setUser')+1]
			del split[split.index('/setUser')+1]
			split.remove('/setUser')
			text = ' '.join(split)
			message['text']=text
			message['from']['id']=senderID

		# CUSTOMIZE FROM HERE
		rep = Responder.respondTo(message, chat_id)
		if rep:
			reply(rep)

app = webapp2.WSGIApplication([
	('/me', MeHandler),
	('/updates', GetUpdatesHandler),
	('/set_webhook', SetWebhookHandler),
	('/webhook', WebhookHandler),
	('/remind', ReminderHandler),
], debug=True)
