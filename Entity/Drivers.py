# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
import datetime


class DriverEntry(ndb.Model):
    event = ndb.KeyProperty(required=True)
    user = ndb.KeyProperty(required=True)

    def delete(self):
        self.key.delete()


def create(event,user):
    entry = DriverEntry(user=user.key, event=event.key)
    entry.put()
    return entry


def getByEvent(event):
    return DriverEntry.query(DriverEntry.event == event.key)


def getByUser(user):
    return DriverEntry.query(DriverEntry.user == user.key)


def getByEventAndUser(event, user):
    return DriverEntry.query(DriverEntry.event == event.key,DriverEntry.user == user.key).get()


def getAllSortedByUser():
    return DriverEntry.query().order(DriverEntry.user)

