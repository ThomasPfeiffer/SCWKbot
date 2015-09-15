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

def createRepeatingEvent(name, place , day, time):
	event = RepeatingEvent.getByDay(day)
	if event:
		return u'Am gegebenen Tag existiert bereits ein wiederholtes Event: \n' + event.toString()	
	event = RepeatingEvent.create(name, place, day, time)
	return u'Wiederholtes Event erstellt: \n' + event.toString()

def create(user, additional):
	if not additional:
		return u'Um ein Event zu erstellen müssen entsprechende Angaben gemacht werden: Name;Ort;Datum/Tag;Zeit)'

	split = additional.split(';')
	if len(split) != 4:
		return u'Anzahl der Argumente ist Falsch! Es müssen 4 sein. (erstelle Name;Ort;Datum/Tag;Zeit)'

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
			day = Event.DAY_DICT[dateOrDayString]
			return createRepeatingEvent(name, place, dateOrDayString, time)
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


def deleteRepeatingEvent(user, additional):
	if additional:
		additional = additional.lower()
	else:
		return u'Um ein wiederholtes Event zu löschen muss dessen Wochentag angegeben werden.' 
	try:
		Event.DAY_DICT[additional]
	except KeyError:
		return u'Um ein wiederholtes Event zu löschen muss dessen Wochentag angegeben werden.' + additional + u' ist nicht gültig.'
	if RepeatingEvent.deleteByDay(additional):
		return u'Wiederholtes event am ' + additional + u' gelöscht'
	return u'Löschen fehlgeschlagen'

def infoRepeatingEvents():
	allReps = RepeatingEvent.getAll()
	if allReps:
		answer = u'Folgende wiederholte Events sind aktiv: '
		for repEvent in allReps:
			answer = answer + u'\n' + repEvent.toString()
	else:
		answer = u' Es sind keine wiederholten Events aktiv.'
	return answer