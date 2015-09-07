# -*- coding: utf-8 -*-
from datetime import datetime
import re
import random
import Entity.User
import Entity.Event
import Logic.UserController as UserController
import main
from google.appengine.ext import ndb


def respondTo(message, sender):

	message_id = message.get('message_id')
	date = message.get('date')
	text = message.get('text')
	sender = message.get('from')
	senderID = str(sender['id'])
	senderFirstName = sender['first_name']
	chat = message['chat']
	chat_id = str(chat['id'])

	# For dev
	if text.startswith('/setUser'):
		split = text.split(' ',3)
		user = Entity.User.get(split[1])
		if not user:
			return u'Error, no user with ID ' + split[1] + u' found'
		senderID = user.key.id()
		senderFirstName = user.firstName
		text = split[2]

	return u'Registration: ' + main.getUserRegistrationEnabled()

	# message.get('text') = split[2]


	# messageSplit = message.lower().split()
	# if len(messageSplit) < 1:
	# 	return

	# command = messageSplit[0]
	# if len(messageSplit) > 1:
	# 	event = getEvent(messageSplit[1])
	# if command.startswith('an') or command.startswith('ab'):			
	# 	if(event):
	# 		if command.startswith('an'):
	# 			return register(sender, event)
	# 		if command.startswith('ab'):
	# 			return cancel(sender, event)
	# 	else:
	# 		return requestEvent(sender)
	return "Folgende befehle sind möglich: \n\tanmelden 'Wochentag' - für nächstes event am angegebenen Wochentag anmelden\n\tabmelden 'Wochentag' - für nächstes event am angegebenen Wochentag anmelden\n\tanmelden 'TT.MM.JJJJ' - für event am angegebenen Datum anmelden\n\tabmelden 'TT.MM.JJJJ' - für event am angegebenen Datum anmelden\n\tanmelden - Liste mit nächsten Events zur Anmeldung\n\tanmelden - Liste mit nächsten Events zur Abmeldung\n\tstatus 'Wochentag' - An- und Abmeldungen nächstes Event am angegebenen Wochentag abrufen\n\tstatus 'TT.MM.JJJJ' - An- und Abmeldungen für Event am angegebenen Datum abrufen\n\tstatus - An- und Abmeldungen für nächstes Event abrufen\n\terstellen 'TT.MM.JJJJ' Event an gegebenem Datum erstellen\n\tabsagen 'TT.MM.JJJJ' Event an gegebenem Datum löschen\n"