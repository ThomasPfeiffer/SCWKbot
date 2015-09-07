# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
import datetime

class Event(ndb.Model):
	name = ndb.StringProperty(required = True)
	place = ndb.StringProperty()
	date = ndb.DateTimeProperty(required = True)

	registeredUsers = ndb.KeyProperty(repeated = True)
	cancelledUsers = ndb.KeyProperty(repeated = True)

	def registerUser(self, userKey):
		if userKey in self.cancelledUsers:
			self.cancelledUsers.remove(userKey)
		if userKey in self.registeredUsers:
			return True
		self.registeredUsers.append(userKey)
		self.put()
		return True

	def cancelUser(self, userKey):
		if userKey in self.registeredUsers:
			self.registeredUsers.remove(userKey)
		if userKey in self.cancelledUsers:
			return True
		self.cancelledUsers.append(userKey)
		self.put()
		return True

	def toString(self):
		return "Name: " + self.name + "\n Ort: " + self.place + "\n Zeit: " + str(self.date)

def create(name, place, date):
	event = Event(name=name, place=place, date = date)
	event.put()
	return event

def deleteByDate(date):
	event = getByDate(date)
	if event:
		event.key.delete()
		return True
	return False

def getByDate(date):
	minimum = datetime.datetime.combine(date, datetime.datetime.min.time())
	maximum = datetime.datetime.combine(date, datetime.datetime.max.time())
	return Event.query(ndb.AND(Event.date >= minimum, Event.date <= maximum)).get()

def getNextEvent():
	event = Event.query().order(-Event.date).fetch(1)
	if event:
		if event.date < datetime.datetime.now().date():
			return None
	return event

def get(eventID):
	return Event.get_by_id(eventID)

