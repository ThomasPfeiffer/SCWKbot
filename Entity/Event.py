# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

class Event(ndb.Model):
    name = ndb.StringProperty(required = True)
    place = ndb.StringProperty()
    date = ndb.DateTimeProperty(required = True)

    registeredUsers = ndb.KeyProperty(repeated = True)
    cancelledUsers = ndb.KeyProperty(repeated = True)

    def toString(self):
    	return "Name: " + self.name + "\n Ort: " + self.place + "\n Zeit: " + str(self.date)

def create(name, place, date):
	event = Event(name=name, place=place, date = date)
	event.put()
	return event

def registerUser(eventID, userKey):
	event = getEvent(eventID)
	if userKey in event.cancelledUsers:
		event.cancelledUsers.remove(userKey)
	if userKey in event.registeredUsers:
		return True
	event.registeredUsers.append(userKey)
	return True

def cancelUser(eventID, userKey):
	event = getEvent(eventID)
	if userKey in event.registeredUsers:
		event.registeredUsers.remove(userKey)
	if userKey in event.cancelledUsers:
		return True
	event.cancelledUsers.append(userKey)
	return True

def getByDate(date):
	return Event.query(Event.date.date == date)

def get(eventID):
	return Event.get_by_id(eventID)