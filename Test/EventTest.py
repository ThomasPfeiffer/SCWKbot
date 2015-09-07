# encoding: utf8

import Entity.Event
import Entity.User
import datetime
import re

def respondTo(message, chat_id, userID = None):

	message_id = message.get('message_id')
	date = message.get('date')
	text = message.get('text').decode('utf-8')
	sender = message.get('from')
	if not userID:
		senderID = str(sender['id'])
	else:
		senderID=userID
	senderFirstName = sender['first_name'].decode('utf-8')
	chat = message['chat']
	chat_id = str(chat['id'])

	if "create" in  text:
		textSplit = text.lower().split(';')
		name = textSplit[1]
		place = textSplit[2]
		dateString = textSplit[3]+" "+textSplit[4]
		try:
			date = datetime.datetime.strptime(dateString, "%d.%m.%Y %H:%M")
		except ValueError as err:
			return u'Die Zeitangabe ' + dateString + u' ist nicht im richtigen Format. (TT.MM.JJJJ SS:MM)'
		event = Entity.Event.getByDate(date)
		if event:
			return u'Am gegebenen Datum existiert bereits ein Event: \n' + event.toString()		
		event = Entity.Event.create(name, place, date)
		return u'Event erstellt: \n' + event.toString()

	if "delete" in  text:
		textSplit = text.lower().split()
		dateString = textSplit[1]
		try:
			date = datetime.datetime.strptime(dateString, "%d.%m.%Y").date()
		except ValueError as err:
			return u'Die Zeitangabe ' + dateString + u' ist nicht im richtigen Format. (TT.MM.JJJJ)'
		if Entity.Event.deleteByDate(date):
			return u'Event am ' + dateString + u' gelöscht.'
		else:
			return u'Kein Event am ' + dateString + u' gefunden.'

	if text.startswith("an"):
		textSplit = text.lower().split()
		command = textSplit[0]
		if len(textSplit) > 1:
			dateString = textSplit[1]
			date = datetime.datetime.strptime(dateString, "%d.%m.%Y").date()
			event = Entity.Event.getByDate(date)
			if not event:
				return u'Kein Event am ' + dateString
			userKey = Entity.User.getKey(senderID)
			if event.registerUser(userKey):
				return senderFirstName + u' für ' + event.name + u' angemeldet.'

	if text.startswith("ab"):
		textSplit = text.lower().split()
		command = textSplit[0]
		if len(textSplit) > 1:
			dateString = textSplit[1]
			date = datetime.datetime.strptime(dateString, "%d.%m.%Y").date()
			event = Entity.Event.getByDate(date)
			if not event:
				return u'Kein Event am ' + dateString
			userKey = Entity.User.getKey(senderID)
			if event.cancelUser(userKey):
				return senderFirstName + u' für ' + event.name + u' abgemeldet.'