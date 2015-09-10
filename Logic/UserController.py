# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import date
from datetime import timedelta
import re
import Entity.User as User
import Entity.Event as Event


def createOrUpdate(senderID, senderFirstName, chat_id):
	user = User.update(senderID, senderFirstName, chat_id)
	if not user:
		user = User.create(senderID, senderFirstName, chat_id)
	return user

def registerForEvent(user, additional):
	return regOrCancel(user, additional, True)

def cancelForEvent(user, additional):
	return regOrCancel(user, additional, False)


def getDateByDay(day):
	d = date.today()
	i = 0
	while d.weekday() != Event.DAY_DICT[day]:
		 d += timedelta(1)
		 i += 1
		 if i > 10:
		 	break
	return d

def regOrCancel(user, additional, reg):
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
		if reg:
			event.registerUser(user.key)
			return user.firstName + u' für ' + event.name + u' am ' + event.date.strftime("%d.%m.%Y %H:%M") + u' angemeldet.'
		else:
			event.cancelUser(user.key)
			return user.firstName + u' für ' + event.name + u' am ' + event.date.strftime("%d.%m.%Y %H:%M") + u' abgemeldet.'
	
	return additional + u' ist keine gültige Eingabe. Möglich sind: \n\tKeine Angabe->Nächstes event\n\tWochentag->Event an diesem Tag\n\tDatum(TT.MM.JJJ)->Event an diesem Datum'
		