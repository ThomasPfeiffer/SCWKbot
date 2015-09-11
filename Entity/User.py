# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

# ================================

class User(ndb.Model):
	firstName = ndb.StringProperty(required = True)
	chatID = ndb.StringProperty()
	admin = ndb.BooleanProperty(default = False)

	def toString(self):
		return "first name: " + self.firstName + ", chatID: " + self.chatID


# ================================

def create(userID, firstName, chatID):
	user = User(firstName = firstName, chatID = chatID,id=userID)
	user.put()
	return user

def update(userID, firstName, chatID):
	user = get(userID)
	if user:
		if user.firstName != firstName or user.chatID != chatID:
			user.firstName = firstName
			user.chatID = chatID
			user.put()
	return user

def get(userID):
	return User.get_by_id(userID)

def delete(userID):
	getKey(userID).delete()

def getKey(userID):
	return ndb.Key(User, userID)

def setAdmin(userID, value):
	user = get(userID)
	if user:
		user.admin = value
		user.put()
		return True

