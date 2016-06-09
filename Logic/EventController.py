# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import date
from datetime import timedelta
import re
import Entity.User as User
import Entity.Event as Event
import Entity.RepeatingEvent as RepeatingEvent
import Responder


def createSingleEvent(name, place, date):
	event = Event.getByDate(date)
	if event:
		return u'Am gegebenen Datum existiert bereits ein Event: \n' + event.toString()	
	event = Event.create(name, place, date)
	return u'Event erstellt: \n' + event.toString()

def createRepeatingEvent(name, place , day, time, endDate):
	rep = RepeatingEvent.create(name, place, day, time, endDate)
	events = rep.createEvents()
	answer = u'Events an diesen Daten erstellt:'
	for created in events[0]:
		answer = answer + u'\n' + created.strftime("%d.%m.%Y")
	if events[1]:
		answer = answer + u'\nFolgende Daten übersprungen, da an diesen schon ein Event existiert:'
		for skipped in events[1]:
			answer = answer + u'\n' + skipped.strftime("%d.%m.%Y")
	return answer

def updateRepeating(user, additional):
	rep = RepeatingEvent.get(int(additional.split[0]))
	events = Event.getByRepeating(rep.key)
	i = 0
	for event in events:
		event.date = event.date + timedelta(minutes=int(additional.split[1]))
		event.put()
		i = i +1
	return str(i) + ' events updated'

def create(user, additional):
	if not additional:
		return u'Um ein Event zu erstellen müssen entsprechende Angaben gemacht werden: Name;[Ort];Datum/Tag;Zeit;[EndDatum])'

	split = additional.split(';')
	if (len(split) != 4) and (len(split) != 5):
		return u'Anzahl der Argumente ist Falsch! Es müssen 4 oder 5 sein. (erstelle Name;[Ort];Datum/Tag;Zeit;[EndDatum])'

	name = split[0]
	if not name:
		return u'Es muss ein Name angegeben werden'
	place = split[1]
	timeString = split[3]
	time = None
	try:
		time = datetime.strptime(timeString, "%H:%M").time()
	except ValueError as err:
		return u'Die Zeitangabe ' + timeString + u'hat das falsche Format (HH:MM).'
	dateOrDayString = split[2]
	try:
		date = datetime.strptime(dateOrDayString, "%d.%m.%Y").date()
		return createSingleEvent(name, place, datetime.combine(date, time))
	except ValueError as err:
		try:
			if dateOrDayString:
				dateOrDayString = dateOrDayString.lower()
			day = Event.DAY_DICT[dateOrDayString]
			try:
				endDateString = split[4]
				if endDateString:
					endDate = datetime.strptime(endDateString, "%d.%m.%Y").date()
				return createRepeatingEvent(name, place, day, time, endDate)
			except ValueError as err2:
				return u'EndDatum hat falsches Format.'
		except KeyError:
			return u'Als drittes Argument muss entweder ein Datum(TT.MM.JJJJ) oder ein Wochentag eingegeben werden'
	return 'Fehler'

def delete(user, additional):
	result = Responder.parseEvent(user, additional)
	if isinstance(result,Event.Event):
			date = result.date
			name = result.name
			result.key.delete()
			return u' Event ' + name + u' am ' + date.strftime("%d.%m.%Y %H:%M") + u' gelöscht.'
	if isinstance(result,basestring):
		return result