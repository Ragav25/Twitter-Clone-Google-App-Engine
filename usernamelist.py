from google.appengine.ext import ndb

class UserNameList(ndb.Model):
    userNames = ndb.StringProperty(repeated=True)
