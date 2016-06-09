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
import Logic.DriverController as DriverController
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
			return u'Es konnte kein in Zukunft stattfindendes Event gefunden werden. Ein Administrator muss erst eines anlegen.'
	else:
		additional = additional.lower()

	if not event:
		if additional in Event.DAY_DICT.keys():
			nextDay = getDateByDay(additional)
			event = Event.getByDate(nextDay)
			if not event:
				return u'Es konnte kein Event am nächsten ' + additional.title() + u' (' + nextDay.strftime("%d.%m.%Y") + u') gefunden werden.'
	if not event:
		try:
			date = datetime.strptime(additional, "%d.%m.%Y").date()
			event = Event.getByDate(date)
			if not event:
				return u'Es konnte kein Event am ' + additional + ' gefunden werden.'
		except ValueError:
			pass
	if event:
		return event
	
	return additional + u' ist keine gültige Eingabe. Möglich sind: \n\tKeine Angabe -> Nächstes event\n\tWochentag -> Event an diesem Tag\n\tDatum(TT.MM.JJJJ) -> Event an diesem Datum'
		


def respondTo(message, sender):

	MAINTENANCE = False

	message_id = message.get('message_id')
	date = message.get('date')
	text = message.get('text')
	sender = message.get('from')
	senderID = str(sender['id'])
	senderFirstName = sender['first_name']
	chat = message['chat']
	chat_id = str(chat['id'])

	logging.info('Message ' + text + ' from ' + senderFirstName + '(' + senderID + ')')

	answer = u''

	if MAINTENANCE:
		if senderID != '13278104':
			return u'SCWKbot wird gerade gewartet!'
		else:
			answer = answer + u'Achtung, Wartung aktiv!\n'

	user = UserController.get(senderID)
	if not user:
		user = User.create(senderID, senderFirstName, chat_id)
	
	textSplit = text.partition(' ')
	command = textSplit[0].lower()
	additional = None
	if textSplit[2]:
		additional = textSplit[2]

	if command.startswith(u'an'):
		return  answer + UserController.registerForEvent(user, additional)

	if command.startswith(u'ab'):
		return  answer + UserController.cancelForEvent(user, additional)

	if command.startswith(u'info'):
		return  answer + UserController.infoForEvent(user, additional)

	if command.startswith(u'fahrtlöschen'):
		return  answer + DriverController.delete(user, additional)
	if command.startswith(u'fahrt'):
		return  answer + DriverController.create(user, additional)

	if user.admin:
		if command.startswith(u'erstell'):
			return  answer + EventController.create(user, additional)
		if command.startswith(u'lösch'):
			return  answer + EventController.delete(user, additional)
		if command.startswith(u'updateRepeating'):
			return  answer + EventController.updateRepeating(user, additional)
		if command.startswith(u'fahrerliste'):
			return  answer + DriverController.listByUser(additional)
	

	
	return answer + getHelpText(user)

def getHelpText(user):
	answer=  u'Folgende befehle sind möglich: \n\t an -> anmelden \n\t ab -> abmelden \n\t info (x)-> Informationen zu einem (oder x) Event(s) \n\n Zusätzlich kann ein bestimmter Tag (z.B. "Montag") oder ein Datum (TT.MM.JJJJ) angegeben werden. Wird nichts angegeben, wird das nächste Training/Spiel genommen.\n\n Um Fahrten einzutragen fahrt TT.MM.JJJJ mit dem Datum des jeweiligen spiels eingeben. Einträge können mit fahrtlöschen TT.MM.JJJJ wieder gelöscht werden.'
	if user.admin:
		answer = answer + u'\n\n Admin befehle: \n\n erstelle Name;(Ort);Datum/Tag;Zeit -> Ein Event erstellen. Angabe von einem Ort ist optional. Wird ein Datum (TT.MM.JJJJ) angegeben, wird ein einzelnes Event erstellt. Wird ein Wochentag angegeben, muss zusätzlich ein Enddatum angegeben werden. Bis zu diesem wird das Event dann jede Woche wiederholt. Die Zeit muss im Format HH:MM angegeben werden. ";" als Trennzeichen, damit auch Leerzeichen möglich sind. Pro Tag ist nur ein Event Möglich. \n \n lösche -> Ein einzelnes Event löschen. Welches wird so angegeben wie bei anmelden/abmelden/info (Wochentag, Datum oder nichts).  \n\n fahrerliste TT.MM.JJJJ-> Fahrten ab angegebenem Datum auflisten.'
	return answer
