# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from datetime import date
from datetime import timedelta
import re
import Entity.User as User
import Entity.Event as Event
import Responder


def get(senderID):
    user = User.get(senderID)
    return user

def registerForEvent(user, additional):
    if additional:
        try:
            date = datetime.strptime(additional, "%d.%m.%Y").date()
            if date < datetime.now().date():
                        return u'Bitte ein Datum in der Zukunft angeben.'
        except ValueError:
            pass
    result = Responder.parseEvent(user, additional)
    if isinstance(result,Event.Event):
            result.registerUser(user.key)
            answer = user.firstName + u' für ' + result.name + u' am ' + result.date.strftime("%d.%m.%Y %H:%M") + u' angemeldet.'
            answer = answer + list_registered_cancelled(result)
            return answer
    if isinstance(result,basestring):
        return result

def cancelForEvent(user, additional):
    if additional:
        try:
            date = datetime.strptime(additional, "%d.%m.%Y").date()
            if date < datetime.now().date():
                        return u'Bitte ein Datum in der Zukunft angeben.'
        except ValueError:
            pass
    result = Responder.parseEvent(user, additional)
    if isinstance(result,Event.Event):
            result.cancelUser(user.key)
            answer = user.firstName + u' für ' + result.name + u' am ' + result.date.strftime("%d.%m.%Y %H:%M") + u' abgemeldet.'
            answer = answer + list_registered_cancelled(result)
            return answer
    if isinstance(result,basestring):
        return result

def infoForEvent(user, additional):
    if additional:
        try:
            amount = int(additional)
            events = Event.getNext(amount)
            answer = ''
            if not events:
                return u'Es konnte kein in Zukunft stattfindendes Event gefunden werden. Ein Administrator muss erst eines anlegen.'
            if len(events) < amount:
                answer += u'Es wurden nur ' + str(len(events)) + u' zukünftige Events gefunden. '
            answer += u'Die nächsten ' + str(len(events)) + ' Events: \n\n'
            for e in events:
                answer += e.toString()
                answer += u'\n\n'
            return answer
        except ValueError:
            pass
    result = Responder.parseEvent(user, additional)
    if isinstance(result,Event.Event):
        answer = result.toString()
        answer = answer + list_registered_cancelled(result)
        return answer
    if isinstance(result,basestring):
        return result

def list_registered_cancelled(event):
    result = u'\n Angemeldet (' + str(len(event.registeredUsers)) + u'): '
    if event.registeredUsers:
        registered = map(lambda userKey: userKey.get().firstName, event.registeredUsers)
        result = result + ','.join(registered)
    else:
        result = result + u'-'
    result = result + u'\n Abgemeldet (' + str(len(event.cancelledUsers)) + u'): '
    if event.cancelledUsers:
        cancelled = map(lambda userKey: userKey.get().firstName, event.cancelledUsers)
        result = result + ','.join(cancelled)
    else:
        result = result + u'-'
    return result

def isAdmin(userID):
    user = User.get(userID)
    if user:
        return user.admin

def deleteUser(senderID, userID):
    if isAdmin(senderID):
        User.delete(userID)
        return True



def setAdmin(senderID, userID, value):
    if isAdmin(senderID):
        return User.setAdmin(userID, value)

