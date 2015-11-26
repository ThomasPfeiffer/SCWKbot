# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import date
from datetime import timedelta
import Entity.Drivers as Drivers
import Entity.Event as Event
import Responder


def create(user, dateString):
	if not dateString:
		return u'Um eine Fahrt anzugeben muss das Datum des Spiels (TT.MM.JJJJ) angegeben werden.'

	date = None
	try:
		date = datetime.strptime(dateString, "%d.%m.%Y").date()
	except ValueError as err:
		return u'Die Datumsangabe ' + dateString + u' hat das falsche Format (HH:MM).'

	event = Event.getByDate(date)
	if not event:
		return u'Es konnte kein Event am ' + dateString + u' gefunden werden.'

	driverEntry = Drivers.getByEventAndUser(event, user)
	if driverEntry:
		return u'Am ' + dateString + u' existiert bereits ein Eintrag für ' + user.firstName

	driverEntry = Drivers.create(event, user)
	if driverEntry:
		return u'Fahrteneintrag für ' + user.firstName + ' erstellt. Event:\n' + event.toString()

	return 'Fehler'

def delete(user, dateString):
	if not dateString:
		return u'Um einen Fahrteneintrag zu löschen muss das Datum des Spiels (TT.MM.JJJJ) angegeben werden.'

	date = None
	try:
		date = datetime.strptime(dateString, "%d.%m.%Y").date()
	except ValueError as err:
		return u'Die Datumsangabe ' + dateString + u' hat das falsche Format (HH:MM).'

	event = Event.getByDate(date)
	if not event:
		return u'Es konnte kein Event am ' + dateString + u' gefunden werden.'

	driverEntry = Drivers.getByEventAndUser(event, user)
	if driverEntry:
		driverEntry.delete()
		return u'Eintrag vom ' + dateString + u' gelöscht.'
	return u'Fehler'

def listByUser(dateString):
	date = None
	try:
		date = datetime.strptime(dateString, "%d.%m.%Y").date()
	except ValueError as err:
		return u'Die Datumsangabe ' + dateString + u' hat das falsche Format (HH:MM).'

	entries = Drivers.getAllSortedByUser()

	if not entries:
		return u'Keine Einträge gefunden.'

	entries = filter(lambda x: x.event.get().date.date() > date, entries)

	if not entries:
			return u'Keine Einträge nach dem ' + dateString + u' gefunden.'
	answer = u'Gefundene Einträge: '
	userName =  ''
	for entry in entries:
		if entry.user.get().firstName != userName:
			userName = entry.user.get().firstName
			answer += u'\n' + userName + u':'
		event = entry.event.get()
		answer += "\n " + event.name + " " + event.place + " " + event.date.strftime("%d.%m.%Y")
	return answer