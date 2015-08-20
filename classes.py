from google.appengine.ext import ndb



class Event(ndb.Model):
    eventName = ndb.StringProperty()
    eventPlace = ndb.StringProperty()
    registered = ndb.StringProperty()
    cancelled = ndb.StringProperty()
    eventTime = ndb.StringProperty()

    eventDate = ndb.DateProperty()
    repetitionEndDate = ndb.DateProperty()

class RegOrCanConversation(ndb.Model):
    userID = ndb.StringProperty()
    userFirstName = ndb.StringProperty()
    initDate = ndb.DateProperty()
    register = ndb.BooleanProperty()

