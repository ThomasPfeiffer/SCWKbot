# -*- coding: utf-8 -*-
from datetime import datetime
import re
import random
import Entity.User as User
import Entity.Event as Event
import Logic.UserController as UserController
import Logic.EventController as EventController
import main
from google.appengine.ext import ndb

def parseEvent(user, additional):
	event = None
	if not additional:
		event = Event.getNextEvent()
		if not event:
			return u'Es konnte kein in Zukunft stattfindendes Event gefunden werden. Ein Administrator muss erst eines anlegen.'
	elif additional in Event.DAY_DICT.keys():
			nextDay = getDateByDay(additional)
			event = Event.getByDate(nextDay)
			if not event:
				return u'Es konnte kein Event am nächsten ' + additional.title() + u' (' + nextDay.strftime("%d.%m.%Y") + u') gefunden werden.'
	else:
		try:
			date = datetime.strptime(additional, "%d.%m.%Y").date()
			if date < datetime.now().date():
				return u'Bitte ein Datum in der Zukunft angeben.'
			event = Event.getByDate(date)
			if not event:
				return u'Es konnte kein Event am ' + additional + ' gefunden werden.'
		except ValueError:
			pass
	if event:
		return event
	
	return additional + u' ist keine gültige Eingabe. Möglich sind: \n\tKeine Angabe->Nächstes event\n\tWochentag->Event an diesem Tag\n\tDatum(TT.MM.JJJ)->Event an diesem Datum'
		

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
	if '/setName' in text:
		split = text.split()
		senderFirstName = split[split.index('/setName')+1]
		del split[split.index('/setName')+1]
		split.remove('/setName')
		text = ' '.join(split)

	if '/setUser' in text:
		split = text.split()
		senderID = split[split.index('/setUser')+1]
		del split[split.index('/setUser')+1]
		split.remove('/setUser')
		text = ' '.join(split)

	user = UserController.createOrUpdate(senderID, senderFirstName, chat_id)
	textLower = text.lower()
	textLowerSplit = textLower.split(' ' , 2)
	command = textLowerSplit[0]
	additional = None
	if len(textLowerSplit) > 1:
		additional = textLowerSplit[1]

	if command.startswith(u'an'):
		return UserController.registerForEvent(user, additional)

	if command.startswith(u'ab'):
		return UserController.cancelForEvent(user, additional)

	if command.startswith(u'info'):
		return UserController.infoForEvent(user, additional)

	if user.admin:
		if command.startswith(u'erstell'):
			return EventController.create(user, additional)
		if command.startswith(u'lösch'):
			return EventController.delete(user, additional)

	

	
	return u'Folgende befehle sind möglich: \n\t an -> anmelden \n\t ab -> abmelden \n\t info (x)-> Informationen zu einem (oder X) Event(s) \n Zusätzlich kann ein bestimmter Tag (z.B. "Montag") oder ein Datum (TT.MM.JJJJ) angegeben werden. Wird nichts angegeben, wird das nächste Training/Spiel genommen.'

