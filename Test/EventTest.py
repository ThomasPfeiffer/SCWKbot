# -*- coding: utf-8 -*-

import Entity.Event
import Entity.User
import datetime
import re

def respondTo(message, chat_id):

	message_id = message.get('message_id')
	date = message.get('date')
	text = message.get('text')
	sender = message.get('from')
	senderID = str(sender['id'])
	senderFirstName = sender['first_name']
	chat = message['chat']
	chat_id = str(chat['id'])

	if "create" in  text:
		textSplit = text.lower().split()
		name = textSplit[1]
		place = textSplit[2]
		dateString = textSplit[3]+" "+textSplit[4]
		try:
			date = datetime.datetime.strptime(dateString, "%d.%m.%Y %H:%M")
		except ValueError as err:
			return "Die Zeitangabe " + dateString + " ist nicht im richtigen Format. (TT.MM.JJJJ SS:MM)"
		event = Entity.Event.getByDate(date)
		if event:
			return "Am gegebenen Datum existiert bereits ein Event: \n" + event.toString()		
		event = Entity.Event.create(name, place, date)
		return "Event erstellt: \n" + event.toString()

	if text.startswith("an"):
		textSplit = text.lower().split()
		command = textSplit[0]
		if len(textSplit) > 1:
			dateString = textSplit[1]
			date = datetime.datetime.strptime(dateString, "%d.%m.%Y").date()
			event = Entity.Event.getByDate(date)
			if not event:
				return "Kein Event am " + dateString
			userKey = Entity.User.getKey(senderID)
			if event.registerUser(userKey):
				return senderFirstName + " für " + event.name + " angemeldet."