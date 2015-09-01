from google.appengine.ext import ndb

# ================================

class User(ndb.Model):
    id = ndb.StringProperty()
    firstName = ndb.StringProperty()


# ================================

def createOrUpdateUser(id, firstName):
	user = User(id=id, firstName = firstName)
    user.put()

def getUser(userID):
    return User.get_by_id(userID)