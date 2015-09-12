# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import date
from datetime import timedelta
import re
import Entity.User as User
import Entity.Event as Event
import Responder


def create(user, additional):
	split = additional.lower().split(';')
	if len(split) not in [4,5]:
		return u'Anzahl der Argumente ist Falsch! Es müssen 4 oder 5 sein. (erstelle Name;Ort;Datum;Zeit(;Wiederholungs-Enddatum))'

	name = split[0]
	place = split[1]
	dateString = split[2]+" "+split[3]
	try:
		date = datetime.strptime(dateString, "%d.%m.%Y %H:%M")
	except ValueError as err:
		return u'Die Zeitangabe ' + dateString + u' ist nicht im richtigen Format. (TT.MM.JJJJ HH:MM)'
	event = Event.getByDate(date)
	if event:
		return u'Am gegebenen Datum existiert bereits ein Event: \n' + event.toString()		
	event = Event.create(name, place, date)
	return u'Event erstellt: \n' + event.toString()

def delete(user, additional):
	result = Responder.parseEvent(user, additional)
	if isinstance(result,Event.Event):
			date = result.date
			name = result.name
			result.key.delete()
			return u' Event ' + name + u' am ' + date.strftime("%d.%m.%Y %H:%M") + u' gelöscht.'
	if isinstance(result,basestring):
		return result