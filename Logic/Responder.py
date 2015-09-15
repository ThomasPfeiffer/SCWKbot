# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import date
from datetime import timedelta
import re
import random
import Entity.User as User
import Entity.Event as Event
import Entity.RepeatingEvent as RepeatingEvent
import Logic.UserController as UserController
import Logic.EventController as EventController
import main
import logging
from google.appengine.ext import ndb

def getDateByDay(day):
	d = date.today()
	i = 0
	while d.weekday() != Event.DAY_DICT[day]:
		 d += timedelta(1)
		 i += 1
		 if i > 10:
		 	break
	return d

def parseEvent(user, additional):
	event = None
	if not additional:
		event = Event.getNextEvent()
		if not event:
			event = RepeatingEvent.createEventOnNextDay()
			if not event:
				return u'Es konnte kein in Zukunft stattfindendes Event gefunden werden. Ein Administrator muss erst eines anlegen.'
	else:
		additional = additional.lower()

	if not event:
		if additional in Event.DAY_DICT.keys():
			nextDay = getDateByDay(additional)
			event = Event.getByDate(nextDay)
			if not event:
				event = RepeatingEvent.createEvent(nextDay)
				if not event:
					return u'Es konnte kein Event am nächsten ' + additional.title() + u' (' + nextDay.strftime("%d.%m.%Y") + u') gefunden werden.'
	if not event:
		try:
			date = datetime.strptime(additional, "%d.%m.%Y").date()
			event = Event.getByDate(date)
			if not event:
				event = RepeatingEvent.createEvent(date)
				if not event:
					return u'Es konnte kein Event am ' + additional + ' gefunden werden.'
		except ValueError:
			pass
	if event:
		return event
	
	return additional + u' ist keine gültige Eingabe. Möglich sind: \n\tKeine Angabe -> Nächstes event\n\tWochentag -> Event an diesem Tag\n\tDatum(TT.MM.JJJJ) -> Event an diesem Datum'
		

def respondTo(message, sender):

	message_id = message.get('message_id')
	date = message.get('date')
	text = message.get('text')
	sender = message.get('from')
	senderID = str(sender['id'])
	senderFirstName = sender['first_name']
	chat = message['chat']
	chat_id = str(chat['id'])

	logging.info('Message ' + text + ' from ' + senderFirstName + '(' + senderID + ')')



	user = UserController.createOrUpdate(senderID, senderFirstName, chat_id)
	textSplit = text.partition(' ')
	command = textSplit[0].lower()
	additional = None
	if textSplit[2]:
		additional = textSplit[2]

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
		if command.startswith(u'beende'):
			return EventController.deleteRepeatingEvent(user, additional)
		if command.startswith(u'wiederhol'):
			return EventController.infoRepeatingEvents()
	

	
	return getHelpText(user)

def getHelpText(user):
	answer=  u'Folgende befehle sind möglich: \n\t an -> anmelden \n\t ab -> abmelden \n\t info (x)-> Informationen zu einem (oder x) Event(s) \n\n Zusätzlich kann ein bestimmter Tag (z.B. "Montag") oder ein Datum (TT.MM.JJJJ) angegeben werden. Wird nichts angegeben, wird das nächste Training/Spiel genommen.'
	if user.admin:
		answer = answer + u'\n\n Admin befehle: \n\n erstelle Name;(Ort);Datum/Tag;Zeit -> Ein Event erstellen. Angabe von einem Ort ist optional. Wird ein Datum (TT.MM.JJJJ) angegeben, wird ein einzelnes Event erstellt. Wird ein Wochentag angegeben, wird das Event jede Woche wiederholt. Die Zeit muss im Format HH:MM angegeben werden. ";" als Trennzeichen, damit auch Leerzeichen möglich sind. Pro Tag ist nur ein Event Möglich. \n \n lösche -> Ein einzelnes Event löschen. Welches wird so angegeben wie bei anmelden/abmelden/info (Wochentag, Datum oder nichts) \n \n beende Wochentag -> Wiederholtes Event an dem Wochentag beenden. \n \n wiederholungen -> Aktive wiederholte Events anzeigen lassen.'
	return answer
