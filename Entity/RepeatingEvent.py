# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
import datetime
import Event
import logging


class Repetition(ndb.Model):
	name = ndb.StringProperty(required = True)
	place = ndb.StringProperty()
	day = ndb.IntegerProperty(required = True)
	time =  ndb.TimeProperty(required = True)
	endDate = ndb.DateProperty(required = True)

	def createEvents(self):
		nextDate = next_weekday(datetime.datetime.now().date(),self.day)
		created = []
		skipped = []
		while(nextDate < self.endDate):
			if not Event.getByDate(nextDate):
				Event.create(self.name,self.place,datetime.datetime.combine(nextDate, self.time),self.key)
				created.append(nextDate)
			else:
				skipped.append(nextDate)
			nextDate += datetime.timedelta(days=7)
		return [created,skipped]

def create(name, place, day, time, endDate):
	repetition = Repetition(name=name, day=day,place=place, time = time, endDate = endDate)
	repetition.put()
	return repetition

def get(eventID):
	return Repetition.get_by_id(eventID)


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)
