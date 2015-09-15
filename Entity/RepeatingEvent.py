# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
import datetime
import Event


class RepeatingEvent(ndb.Model):
	name = ndb.StringProperty(required = True)
	place = ndb.StringProperty()
	day = ndb.StringProperty(required = True, choices=Event.DAY_DICT.keys())
	time = ndb.TimeProperty(required = True)

	def toString(self):
		return "Name: " + self.name + "\n Ort: " + self.place + "\n Tag: " + self.day.title() + "\n Zeit: " + self.time.strftime("%H:%M")

def getAll():
	return RepeatingEvent.query().fetch()

def create(name, place, day, time):
	check = getByDay(day)
	if check:
		raise ValueError('RepeatingEvent on given day exists')
	repeatingEvent = RepeatingEvent(name=name, place=place, day = day, time = time)
	repeatingEvent.put()
	return repeatingEvent

def getByDay(day):
	return RepeatingEvent.query(RepeatingEvent.day == day).get()

def deleteByDay(day):
	repeatingEvent = getByDay(day)
	if repeatingEvent:
		repeatingEvent.key.delete()
		return True
	return False

def createEvent(date):
	day = Event.dayStringForInt(date.weekday())
	repEvent = getByDay(day)
	if repEvent:
		check = Event.getByDate(date)
		if check:
			raise ValueError('Event on given date exists already.')
		return Event.create(repEvent.name, repEvent.place, datetime.datetime.combine(date, repEvent.time))

def createEventOnNextDay():
	now = datetime.datetime.today()
	day = now.weekday()
	dayP7 = day + 7
	while day < dayP7:
		repeatingEvent = getByDay(Event.dayStringForInt(day))
		if repeatingEvent:
			return Event.create(repeatingEvent.name, repeatingEvent.place, datetime.datetime.combine(now.date(), repeatingEvent.time))
		day += 1;
		now = now + datetime.timedelta(days=1)

