# -*- coding: utf-8 -*-
from datetime import datetime
import re
import random

class Event():
    eventName = None
    eventPlace = None
    registered = None
    cancelled = None
    eventTime = None

    eventDate = None
    repetitionEndDate = None

class RegOrCanConversation():
    userID = None
    userFirstName = None
    initDate = None
    register = None


def getEvent(msgText):
	#Kein Datum in vergangenheit
	return

def register(sender, event):
	return

def cancel(sender, event):
	return

def requestEvent(sender):
	return

def eventCreation(message, sender, event):
	if not event.eventName:
		event.eventName = message
	if not event.eventPlace:
		event.eventPlace = message
	if not event.eventTime:
		event.eventTime = message
	if not event.repetitionEndDate
		event.repetitionEndDate = parseDate(message)


def respondTo(message, sender, date):
	if not message:
		return
	messageSplit = message.lower().split()
	if len(messageSplit) < 1:
		return

	command = messageSplit[0]
	if len(messageSplit) > 1:
		event = getEvent(messageSplit[1])
	if command.startswith('an') or command.startswith('ab'):			
		if(event):
			if command.startswith('an'):
				return register(sender, event)
			if command.startswith('ab'):
				return cancel(sender, event)
		else:
			return requestEvent(sender)
	return "Folgende befehle sind möglich: \n\tanmelden 'Wochentag' - für nächstes event am angegebenen Wochentag anmelden\n\tabmelden 'Wochentag' - für nächstes event am angegebenen Wochentag anmelden\n\tanmelden 'TT.MM.JJJJ' - für event am angegebenen Datum anmelden\n\tabmelden 'TT.MM.JJJJ' - für event am angegebenen Datum anmelden\n\tanmelden - Liste mit nächsten Events zur Anmeldung\n\tanmelden - Liste mit nächsten Events zur Abmeldung\n\tstatus 'Wochentag' - An- und Abmeldungen nächstes Event am angegebenen Wochentag abrufen\n\tstatus 'TT.MM.JJJJ' - An- und Abmeldungen für Event am angegebenen Datum abrufen\n\tstatus - An- und Abmeldungen für nächstes Event abrufen\n\terstellen 'TT.MM.JJJJ' Event an gegebenem Datum erstellen\n\tabsagen 'TT.MM.JJJJ' Event an gegebenem Datum löschen\n"

		

def loop():
	msg = raw_input("sach an: \n")
	print(respondTo(msg, "Thomas", datetime.today().date()))
	loop()


loop()