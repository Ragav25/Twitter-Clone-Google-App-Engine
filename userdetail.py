from google.appengine.ext import ndb

class UserDetail(ndb.Model):
    userName = ndb.StringProperty()
    dateOfBirth = ndb.DateProperty()
    shortProfile = ndb.StringProperty()
