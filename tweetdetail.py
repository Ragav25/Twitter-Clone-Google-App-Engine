from google.appengine.ext import ndb
import datetime

class TweetDetail(ndb.Model):
    newTweets = ndb.StringProperty(repeated=True)
    dateOfBirth = ndb.DateProperty()
    shortProfile = ndb.StringProperty()

    followingUser = ndb.StringProperty(repeated=True)
    followers = ndb.StringProperty(repeated=True)
