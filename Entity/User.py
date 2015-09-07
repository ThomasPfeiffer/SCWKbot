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

def get(userID):
	return User.get_by_id(userID)

def delete(userID):
	getKey(userID).delete()

def getKey(userID):
	return ndb.Key(User, userID)

